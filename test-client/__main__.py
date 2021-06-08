# __main__.py
# Python implementation of the GRPC otg client


from __future__ import print_function
import argparse
import logging
import os
import datetime
import time

# gRPC stuffs
import grpc
from .autogen import otg_pb2
from .autogen import otg_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import json_format

# Json & Ohters
import json


class OpenapiClient():

    def __init__(self, args):
        super().__init__()
    
        self.logger = logging.getLogger(args.logfile) 
        self.server_address = "{}:{}".format(args.target_host, args.target_port)
        
        self.logger.info("Connecting servar at {}".format(self.server_address))

        self.api_initialized = False

    def SetConfig(self, create_option):

        protoRequest = None

        if (create_option == 1):
            # create from json
            jsonRequest = """
            {
                "ports": [
                    {
                    "location": "10.74.45.189;1;1",
                    "name": "tx"
                    }
                ],
                "options": {
                    "port_options": {
                    "location_preemption": true
                    }
                },
                "devices": [
                    {
                        "container_name": "tx",
                        "name": "Device Group",
                        "ethernet": {
                            "name": "Ethernet"
                        }
                    }
                ]
            }
            """
            # self.logger.info("SetConfig [From Json] :: Config (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.Config())
        else:
            self.logger.info("Not implemented!!")
     
        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)
                
            #self.logger.info("Send SetConfig :: Config (protobuff) = {}".format(protoRequest))

            self.logger.info("Sending Configuration and waiting for response ...")

            response = stub.SetConfig(otg_pb2.SetConfigRequest(config=protoRequest))
            self.logger.info("Received Response: Warning = {}, Error = {}".format(response.warnings, response.errors))

    def SetTransmitState(self, create_option):

        protoRequest = None

        if (create_option == 1):
            # create from json
            jsonRequest = """
            {
                "flow_names": null,
                "state" : "START"
            }
            """
            self.logger.info("SetTransmitState [From Json] :: TransmitState (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.TransmitState())
        else:
            # build up protobuff request
            protoRequest = otg_pb2.TransmitState(state=otg_pb2.TransmitState.State.start, flow_names=None)
        
        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)
                
            self.logger.info("Send SetTransmitState :: TransmitState (protobuff) = {}".format(protoRequest))
            
            self.logger.info("Sending Start request and waiting for response ...")

            response = stub.SetTransmitState(otg_pb2.SetTransmitStateRequest(transmit__state=protoRequest))
            self.logger.info("Received Response: Warning = {}, Error = {}".format(response.warnings, response.errors))

def serve(args):
    args.logfile = init_logging(args.logfile)
    client_logger = logging.getLogger(args.logfile) 

    client_logger.info("Starting client ...")
    print("Starting client ...")   
    client = OpenapiClient(args)

    client_logger.info("Testing SetConfig")
    client.SetConfig(1)

    client_logger.info("Testing SetTransmitState")
    client.SetTransmitState(1)

    client_logger.info("Client closed.")
    print("Client closed.")   

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
    parser.add_argument('--target-host', help='target gRPC server host address',
                        default='localhost',
                        type=str)
    parser.add_argument('--target-port', help='target gRPC server port number',
                        default=40051,
                        type=int)
    parser.add_argument('--logfile', help='logfile name [date and time auto appended]',
                        default='gRPCClient',
                        type=str)    

    args = parser.parse_args()

    print ("Args = {}".format(args))

    serve(args)
        