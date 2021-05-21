# __main__.py
# Python implementation of the GRPC otg server

from concurrent import futures

import grpc

from .autogen import otg_pb2
from .autogen import otg_pb2_grpc


import snappi
from google.protobuf import json_format

import argparse

# Json utils
import logging
import json


class Openapi(otg_pb2_grpc.OpenapiServicer):

    def __init__(self, app_mode, target_host, target_port):
        super().__init__()
    
        self.app_mode = app_mode
        self.target_address = "{}:{}".format(target_host, target_port)
        self.api_initialized = False

    def SetConfig(self, request, context):
        #print("Received request.config (string) = {}".format(request.config.SerializeToString()))
        
        jsonObj = json_format.MessageToJson(request.config, including_default_value_fields=True, preserving_proto_field_name=True)
        #print("Received request.config (JSON) = {}".format(jsonObj))

        # for snappy
        if self.api_initialized == False:
            self.api = snappi.api(host=self.target_address, ext=self.app_mode)
            # clean up any old session
            if getattr(self.api, 'assistant', None) is not None:
                # print("*** Deleting old session ...")
                self.api.assistant.Session.remove()

            self.api_initialized = True
        response = self.api.set_config(jsonObj)

        return (json_format.Parse(response.serialize(), otg_pb2.Details()))

    def SetLinkState(self, request, context):
        #print("Received request.link__state (string) = {}".format(request.link__state.SerializeToString()))

        jsonObj = json_format.MessageToJson(request.link__state, including_default_value_fields=True, preserving_proto_field_name=True)
        #print("Received request.link__state (JSON) = {}".format(jsonObj))

        # for snappy
        response = self.api.set_link_state(jsonObj)

        return (json_format.Parse(response.serialize(), otg_pb2.Details()))

    def SetTransmitState(self, request, context):
        #print("Received request.transmit__state (string) = {}".format(request.transmit__state.SerializeToString()))
        
        jsonObj = json_format.MessageToJson(request.transmit__state, including_default_value_fields=True, preserving_proto_field_name=True)
        #print("Received request.transmit__state (JSON) = {}".format(jsonObj))

        # for snappy
        response = self.api.set_transmit_state(jsonObj)

        return (json_format.Parse(response.serialize(), otg_pb2.Details()))

    def GetMetrics(self, request, context):
        #print("Received request.metrics__request (string) = {}".format(request.metrics__request.SerializeToString()))

        jsonObj = json_format.MessageToJson(request.metrics__request, including_default_value_fields=True, preserving_proto_field_name=True)
        #print("Received request.metrics__request (JSON) = {}".format(jsonObj))

        # for snappy
        response = self.api.get_metrics(jsonObj)

        return json_format.Parse(response.serialize(), otg_pb2.MetricsResponse())


def serve(server_port, app_mode, target_host, target_port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    otg_pb2_grpc.add_OpenapiServicer_to_server(Openapi(app_mode, target_host, target_port), server)
    
    server_address = "[::]:{}".format(server_port)
    app_name = "Athena"
    if (app_mode == 'ixnetwork'):
        app_name = 'IxNetwork'
    print("gRPC Server ({} - OpenApi) starting at {} ...".format(app_name, server_address))
    print("Target {} address:  {}:{}".format(app_name, target_host, target_port))
    
    server.add_insecure_port(server_address)
    server.start()

    print("gRPC Server Started.", flush=True)

    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()    
    

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
    args = parser.parse_args()

    # print ("Args = {}".format(args))

    serve(args.server_port, args.app_mode, args.target_host, args.target_port)
        