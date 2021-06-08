# __main__.py
# Python implementation of the GRPC otg server

from concurrent import futures

import grpc

from .autogen import otg_pb2
from .autogen import otg_pb2_grpc


import snappi
from google.protobuf import json_format

import argparse
import logging
import os
import datetime
import time

# Json utils
import json


class Openapi(otg_pb2_grpc.OpenapiServicer):

    def __init__(self, args):
        super().__init__()
    
        self.logger = logging.getLogger(args.logfile) 

        self.app_mode = args.app_mode
        self.target_address = "{}:{}".format(args.target_host, args.target_port)
        self.api_initialized = False

    def SetConfig(self, request, context):
        #self.logger.info("Received request.config (string) = {}".format(request.config.SerializeToString()))
        
        jsonObj = json_format.MessageToJson(request.config, including_default_value_fields=True, preserving_proto_field_name=True)
        #self.logger.info("Received request.config (JSON) = {}".format(jsonObj))

        # for snappy
        if self.api_initialized == False:
            if self.app_mode == 'ixnetwork':
                target = "http://{}".format(self.target_address)
                self.api = snappi.api(host=target, ext=self.app_mode)
                self.logger.info("Snappi Remote Server address = {} in IxNetwork mode".format(target))
            else:
                target = "https://{}".format(self.target_address)
                self.api = snappi.api(host=target)
                self.logger.info("Snappi Remote Server address = {} in Athena mode".format(target))

            self.api_initialized = True
            self.logger.info('Snappi initialized')

        
        self.logger.info("Requesting set_config ...")
        response = self.api.set_config(jsonObj)
        #self.logger.info("Received Reply from Remote Server (JSON) = {}".format(response))

        return (json_format.Parse(response.serialize(), otg_pb2.Details()))

    def SetLinkState(self, request, context):
        #self.logger.info("Received request.link__state (string) = {}".format(request.link__state.SerializeToString()))

        jsonObj = json_format.MessageToJson(request.link__state, including_default_value_fields=True, preserving_proto_field_name=True)
        #self.logger.info("Received request.link__state (JSON) = {}".format(jsonObj))

        # for snappy
        self.logger.info("Requesting SetLinkState ...")
        response = self.api.set_link_state(jsonObj)
        #self.logger.info("Received Reply from Remote Server (JSON) = {}".format(response))

        return (json_format.Parse(response.serialize(), otg_pb2.Details()))

    def SetTransmitState(self, request, context):
        #self.logger.info("Received request.transmit__state (string) = {}".format(request.transmit__state.SerializeToString()))
        
        jsonObj = json_format.MessageToJson(request.transmit__state, including_default_value_fields=True, preserving_proto_field_name=True)
        #self.logger.info("Received request.transmit__state (JSON) = {}".format(jsonObj))

        # for snappy
        self.logger.info("Requesting SetTransmitState ...")
        response = self.api.set_transmit_state(jsonObj)
        #self.logger.info("Received Reply from Remote Server (JSON) = {}".format(response))

        return (json_format.Parse(response.serialize(), otg_pb2.Details()))

    def GetMetrics(self, request, context):
        #self.logger.info("Received request.metrics__request (string) = {}".format(request.metrics__request.SerializeToString()))

        jsonObj = json_format.MessageToJson(request.metrics__request, including_default_value_fields=True, preserving_proto_field_name=True)
        #self.logger.info("Received request.metrics__request (JSON) = {}".format(jsonObj))

        # for snappy
        self.logger.info("Requesting GetMetrics ...")
        response = self.api.get_metrics(jsonObj)
        #self.logger.info("Received Reply from Remote Server (JSON) = {}".format(response))

        return json_format.Parse(response.serialize(), otg_pb2.MetricsResponse())


def serve(args):
    args.logfile = init_logging(args.logfile)
    server_logger = logging.getLogger(args.logfile) 

    app_name = "Athena"
    if (args.app_mode == 'ixnetwork'):
        app_name = 'IxNetwork'

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    otg_pb2_grpc.add_OpenapiServicer_to_server(Openapi(args), server)
    
    server_address = "[::]:{}".format(args.server_port)
    
    if args.insecure == True:
        server_logger.info("Enabling insecure channel")
        server.add_insecure_port(server_address)
        server_logger.info("Enabled insecure channel")
    else:
        server_logger.info("Enabling secure channel")
        private_key = None
        certificate_chain = None
        with open(args.server_key, 'rb') as f:
            private_key = f.read()                
        with open(args.server_crt, 'rb') as f:
            certificate_chain = f.read()

        if private_key != None and certificate_chain != None:
            server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )
            server.add_secure_port(server_address, server_credentials)
            server_logger.info("Enabled secure channel")
        else:
            server_logger.error("Cannot create secure channel, need openssl key. You can generate it with below openssl command")
            server_logger.error("openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -subj '/CN=test.local'")
            
    server_logger.info("Starting gRPC server on %s [App: %s, Target: %s:%s]", server_address, app_name, args.target_host, args.target_port)

    server.start()

    print("gRPC Server Started.", flush=True)

    server.wait_for_termination()

    print("Server closed gracefully")   

def get_current_time():
    current_utc = datetime.datetime.utcnow()
    current_utc = str(current_utc).split('.')[0]
    current_utc = current_utc.replace(' ','-')
    current_utc = current_utc.replace(':','-')
    return current_utc


def init_logging(logger_name, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    logfile = logger_name+'-'+str(get_current_time())+'.log'
    logs_dir = os.path.join(os.path.curdir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    logfile = os.path.join(logs_dir, logfile)  
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(logfile, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    #l.addHandler(streamHandler)  
    return logger_name 

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-port', help='gRPC server port number',
                        default=40051,
                        type=int)
    parser.add_argument('--app-mode', help='target Application mode)',
                        choices=['ixnetwork', 'athena'],
                        default='ixnetwork',
                        type=str)
    parser.add_argument('--target-host', help='target host address',
                        default='localhost',
                        type=str)
    parser.add_argument('--target-port', help='target port number',
                        default=11009,
                        type=int)
    parser.add_argument('--logfile', help='logfile name [date and time auto appended]',
                        default='gRPCServer',
                        type=str)    
    parser.add_argument('--insecure', help='disable TSL security, by default enabled',
                        default=True,
                        action='store_true')
    parser.add_argument('--server-key', help='path to private key, default is server.key',
                        default='server.key',
                        type=str)
    parser.add_argument('--server-crt', help='path to certificate key, default is server.crt',
                        default='server.crt',
                        type=str)
    args = parser.parse_args()

    #print ("Args = {}".format(args))

    serve(args)
        