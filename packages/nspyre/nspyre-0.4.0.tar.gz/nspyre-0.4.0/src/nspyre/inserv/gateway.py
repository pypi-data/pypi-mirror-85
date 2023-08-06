"""
This module manages and centralizes connections to one or more instrument
servers. All instrument server connections should be done through the
InservGateway class.

Author: Jacob Feder
Date: 7/11/2020
"""

###########################
# imports
###########################

# std
import os
import logging

# 3rd party
import parse
import pymongo
from pymongo.errors import PyMongoError
import rpyc

# nspyre
from nspyre.utils.misc import register_quantity_brining
from nspyre.config.config_files import get_config_param, load_config
from nspyre.definitions import MONGO_CONNECT_TIMEOUT, \
                            MONGO_SERVERS_KEY, MONGO_SERVERS_SETTINGS_KEY, \
                            MONGO_RS, RPYC_CONN_TIMEOUT, RPYC_SYNC_TIMEOUT, \
                            INSERV_DEV_ACCESSOR
from nspyre.definitions import Q_

# for properly serializing/deserializing quantity objects using the local
# pint unit registry
register_quantity_brining(Q_)

###########################
# exceptions
###########################

class InservGatewayError(Exception):
    """General InservGateway exception"""
    def __init__(self, msg):
        super().__init__(msg)

###########################
# classes / functions
###########################

# Temporary monkey patching of rpyc to implement synchronous about_to_disconnect feature
# Need to define consts.HANDLE_ABOUT_TO_CLOSE before consts is import by protocol (this is done
# in the load of nspyre.inser.inserv)
import nspyre.inserv.inserv
from rpyc.core.protocol import consts

# Need to monkey patch VoidService for rpyc.utils.factory.connect_stream
from rpyc.core.service import Service
Service._protocol = nspyre.inserv.inserv.InstrumentConnection
Service = nspyre.inserv.inserv.InstrumentService
from rpyc.core.service import VoidService
VoidService = nspyre.inserv.inserv.VoidInstrumentService


class InservGateway():
    """Loads a configuration file, then attempts to connect to all 
    instrument servers

    This class is a representation of the instrument server from the
    client's perspective. It contains server connection information, and an
    instance variable object for each device connected to the remote instrument
    server
    """
    def __init__(self, config_file, mongo_addr=None):
        # config dictionary
        self.config = {}
        # dictionary of available rpyc instrument servers
        # key is the server string id, value is a tuple (rpyc conn, bg thread)
        # e.g. {'local1': (rpyc.core.protocol.Connection, 
        #                  rpyc.utils.helpers.BgServingThread),
        #       'remote1': ...}
        self._servers = {}
        self.mongo_addr = None
        self.mongo_client = None
        self.config = None
        self.update_config(config_file)
        self.config_mongo(mongo_addr)
        self.connect_servers()

    def config_mongo(self, mongo_addr=None):
        """Set up the mongodb database (but connection won't take place until
        a query is made)"""
        if mongo_addr:
            self.mongo_addr = mongo_addr
        else:
            self.mongo_addr,_ = get_config_param(self.config, ['mongodb_addr'])
        logging.info('connecting to mongodb server [{}]...'.\
                            format(self.mongo_addr))
        self.mongo_client = pymongo.MongoClient(mongo_addr,
                            replicaset=MONGO_RS,
                            serverSelectionTimeoutMS=MONGO_CONNECT_TIMEOUT)

    def connect_servers(self):
        """Auto discover and attempt connection to all of the instrument
        servers in mongodb"""
        # retrieve all of the instrument server settings from mongo
        try:
            all_db_names = self.mongo_client.list_database_names()
        except PyMongoError:
            raise InservGatewayError('Failed connecting to mongodb [{}]'.\
                                        format(self.mongo_addr)) from None
        logging.info('connected to mongodb server [{}]'.format(self.mongo_addr))
        for db_name in all_db_names:
            server_name = parse.parse(MONGO_SERVERS_KEY, db_name)
            # filter out all of the dbs that aren't instrument servers
            if server_name:
                # if the name was extracted successfully,
                # get it's value as a string
                server_name = server_name[0]
                # retrieve the server settings dictionary
                db_entry = self.mongo_client[db_name]\
                                    [MONGO_SERVERS_SETTINGS_KEY].find_one()
                self.connect_server(server_name,
                                    db_entry['address'],
                                    db_entry['port'])

    def disconnect_servers(self):
        """Attempt disconnection from all of the instrument servers"""
        for s in list(self._servers):
            self.disconnect_server(s)

    def connect_server(self, s_id, s_addr, s_port):
        """Attempt connection to an instrument server"""
        try:
            # connect to the rpyc server running on the instrument server
            # and start up a background thread to fullfill requests on the
            # client side
            conn = rpyc.connect(s_addr, s_port,
                            config={'allow_pickle' : True,
                                    'timeout' : RPYC_CONN_TIMEOUT,
                                    'sync_request_timeout': RPYC_SYNC_TIMEOUT})

            bg_serving_thread = rpyc.BgServingThread(conn)
            
            # this allows the instrument server to have full access to this
            # client's object dictionaries - appears necessary for lantz
            conn._config['allow_all_attrs'] = True

            self._servers[s_id] = (conn, bg_serving_thread)
        except BaseException:
            raise InservGatewayError('Failed to connect to '
                            'instrument server [{}] at address [{}]'.\
                            format(s_id, s_addr)) from None
        logging.info('instrument server gateway connected to instrument '
                    'server [{}]'.format(s_id))

    def disconnect_server(self, s_id):
        """Disconnect from an instrument server and remove it's associated 
        devices"""
        try:
            conn = self._servers[s_id][0]
            bg_serving_thread = self._servers[s_id][1]
            bg_serving_thread.stop()
            conn.close()
            del self._servers[s_id]
        except BaseException:
            raise InservGatewayError('Failed to disconnect from '
                            'instrument server [{}]'.format(s_id)) from None
        logging.info('instrument server gateway disconnected '
                        'from server [{}]'.format(s_id))

    def servers(self):
        """Return a dictionary containing 'server name' mapped to
        an rpyc conn object"""
        servers_dict = {}
        for s in self._servers:
            servers_dict[s] = self._servers[s][0]

        return servers_dict

    def __getattr__(self, attr):
        """Allow the user to access the server objects directly using
        e.g. gateway.server1.sig_gen.frequency notation"""
        if attr in self._servers:
            return self._servers[attr][0].root
        else:
            raise AttributeError('\'{}\' object has no attribute \'{}\''.\
                        format(self.__class__.__name__, attr))

    def update_config(self, filename):
        """Reload the config file"""
        self.config = load_config(filename)

    def __enter__(self):
        """Python context manager setup"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Python context manager teardown"""
        self.disconnect_servers()

if __name__ == '__main__':
    # configure server logging behavior
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s -- %(levelname)s -- %(message)s',
                        handlers=[logging.StreamHandler()])
    # TODO unit testing module
    with InservGateway() as im:
        pass
        # sg_loc = 'local1/fake_sg'
        # im.devs[sg_loc].amplitude = Q_(2.0, 'volt')
        # im.devs[sg_loc].amplitude = Q_(10.0, 'volt')
        # im.devs[sg_loc].dout[1] = Q_(0.0, 'volt')
        # im.devs[sg_loc].dout[2] = Q_(2.0, 'volt')
        # im.devs[sg_loc].dout[3] = Q_(3.0, 'volt')
        # im.devs[sg_loc].dout[1] = Q_(1.0, 'volt')
        #print('found devices:\n{}'.format(im.devs))
        #print(Q_(5, 'volt') + im.devs[sg_loc].amplitude)
