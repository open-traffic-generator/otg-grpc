# Python implementation of gRPC Test Client

from __future__ import print_function
import argparse
import logging
import os
from pathlib import Path
import datetime
import time

# gRPC stuffs
import grpc
#from .autogen import otg_pb2
#from .autogen import otg_pb2_grpc
from grpc_server.autogen import otg_pb2, otg_pb2_grpc
from google.protobuf import empty_pb2

# Json
import json
from google.protobuf import json_format

#from .common.utils import *
from grpc_server.common.utils import *

# set API version
OTG_API_Version="0.4.10"

class OtgClient():

    def __init__(self, args):
        super().__init__()
    
        self.logger = logging.getLogger(args.logfile) 
        self.server_address = "{}:{}".format(args.target_host, args.target_port)
        self.app_mode = args.app_mode
        self.config_mode = args.config_mode
        
        self.logger.info("Client connecting to gRPC server at {}".format(self.server_address))

        self.api_initialized = False

    def SetConfig(self):

        protoRequest = None
        filename = "config_{}_{}.json".format(self.app_mode, self.config_mode)
        filepath = os.path.join(os.path.dirname(__file__),"config", filename)

        if Path(filepath).is_file == False:
            self.logger.error("SetConfig :: Config File = {} does not exist. Operation Failed !".format(filepath))
            return

        with open(filepath,'r') as jsonfile:
            jsonObj = json.load(jsonfile)
            jsonRequest = json.dumps(jsonObj)

            self.logger.debug("SetConfig [From Json] :: Config (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.Config())

        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)

            self.logger.debug("SetConfig :: SetConfigRequest (protobuf) = {}".format(protoRequest))

            self.logger.debug("Sending Configuration and waiting for response ...")

            try:
                response = stub.SetConfig(otg_pb2.SetConfigRequest(config=protoRequest))
            except grpc.RpcError as e:
                self.logger.error("gRPC Exception Code: {}, Details: {}".format(e.code(), e.details()))
            else:
                self.logger.info("Received Response: {}, Success: {}".format(response, response.HasField("status_code_200")))

    def GetConfig(self):

        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)

            self.logger.debug("Sending GetConfigRequest request and waiting for response ...")

            try:
                empty = otg_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
                response = stub.GetConfig(empty)
            except grpc.RpcError as e:
                self.logger.error("gRPC Exception Code: {}, Details: {}".format(e.code(), e.details()))
            else:
                self.logger.info("Received Response: {}, Success: {}".format(response, response.HasField("status_code_200")))


    def SetTransmitState(self, start):

        protoRequest = None

        if (start == True) :
            # create from json
            jsonRequest = """
            {
                "flow_names": null,
                "state" : "start"
            }
            """
            self.logger.debug("SetTransmitState :: TransmitState (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.TransmitState())
        else:
            # create from json
            jsonRequest = """
            {
                "flow_names": null,
                "state" : "stop"
            }
            """
            self.logger.debug("SetTransmitState :: TransmitState (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.TransmitState())

        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)

            self.logger.debug("SetTransmitState :: TransmitState (protobuf) = {}".format(protoRequest))
          
            self.logger.debug("Sending Start/Stop request and waiting for response ...")
            try:
                response = stub.SetTransmitState(otg_pb2.SetTransmitStateRequest(transmit_state=protoRequest))
            except grpc.RpcError as e:
                self.logger.error("gRPC Exception Code: {}, Details: {}".format(e.code(), e.details()))
            else:
                self.logger.info("Received Response: {}, Success: {}".format(response, response.HasField("status_code_200")))


    def SetLinkState(self, up):

        protoRequest = None

        if (up == True) :
            # create from json
            jsonRequest = """
            {
                "state" : "up"
            }
            """
            self.logger.debug("SetLinkState :: LinkState (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.LinkState())
        else:
            # create from json
            jsonRequest = """
            {
                "state" : "down"
            }
            """
            self.logger.debug("SetLinkState :: LinkState (JSON) = {}".format(jsonRequest))
            protoRequest = json_format.Parse(jsonRequest, otg_pb2.LinkState())

        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)

            self.logger.debug("SetLinkState :: LinkState (protobuf) = {}".format(protoRequest))
          
            self.logger.debug("Sending SetLinkState Up/Down request and waiting for response ...")
            try:
                response = stub.SetLinkState(otg_pb2.SetLinkStateRequest(link_state=protoRequest))
            except grpc.RpcError as e:
                self.logger.error("gRPC Exception Code: {}, Details: {}".format(e.code(), e.details()))
            else:
                self.logger.info("Received Response: {}, Success: {}".format(response, response.HasField("status_code_200")))


    def GetMetrics(self):
        protoRequest = None

        # create from json
        jsonRequest = """
        {
            "choice" : "flow",
            "flow" : {
                "flow_names" : ["p1->p2"],
                "metric_names" : ["frames_tx", "frames_rx"]
            }
        }
        """
        self.logger.debug("GetMetrics :: MetricsRequest (JSON) = {}".format(jsonRequest))
        protoRequest = json_format.Parse(jsonRequest, otg_pb2.MetricsRequest())

        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)

            self.logger.debug("Sending GetMetrics request and waiting for response ...")

            try:
                response = stub.GetMetrics(otg_pb2.GetMetricsRequest(metrics_request = protoRequest))
            except grpc.RpcError as e:
                self.logger.error("gRPC Exception Code: {}, Details: {}".format(e.code(), e.details()))
            else:
                self.logger.info("Received Response: {}".format(response))

    def GetStateMetrics(self):

        with grpc.insecure_channel(self.server_address) as channel:
            stub = otg_pb2_grpc.OpenapiStub(channel)

            self.logger.debug("Sending GetStateMetrics request and waiting for response ...")

            try:
                empty = otg_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
                response = stub.GetStateMetrics(empty)
            except grpc.RpcError as e:
                self.logger.error("gRPC Exception Code: {}, Details: {}".format(e.code(), e.details()))
            else:
                self.logger.info("Received Response: {}".format(response))



def serve(args):
    log_level = logging.INFO
    if args.log_debug == True:
        log_level = logging.DEBUG
    args.logfile = init_logging(args.logfile, log_level, args.log_stdout)

    client_logger = logging.getLogger(args.logfile) 

    client_logger.info("Starting gRPC Client [OTG API Version = {}] ...".format(OTG_API_Version))
    client = OtgClient(args)
    
    client_logger.info("Do SetConfig")
    client.SetConfig()

    if args.app_mode == "athena":
        client_logger.info("Do GetConfig")
        client.GetConfig()

        client_logger.info("Do Start Transmit")
        client.SetTransmitState(True)

        client.GetMetrics()

        client_logger.info("Do Stop Transmit")
        client.SetTransmitState(False)


        #client.GetStateMetrics()

    
    else:
        client_logger.info("Do LinkState Up/Down")
        client.SetLinkState(False)
        client.SetLinkState(True)

        client_logger.info("Do Start Transmit")
        client.SetTransmitState(True)

        client_logger.info("Do Stop Transmit")
        client.SetTransmitState(False)

    client_logger.info("Client closed.")


if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--target-host', help='target gRPC server host address',
                        default='localhost',
                        type=str)
    parser.add_argument('--target-port', help='target gRPC server port number',
                        default=40071,
                        type=int)
    parser.add_argument('--app-mode', help='target Application mode)',
                        choices=['ixnetwork', 'athena'],
                        default='ixnetwork',
                        type=str)
    parser.add_argument('--config-mode', help='target Configuration mode)',
                        choices=['default', 'protocol', 'traffic', 'combined', 'minimal'],
                        default='default',
                        type=str)
    parser.add_argument('--logfile', help='logfile name [date and time auto appended]',
                        default='test_client',
                        type=str)    
    parser.add_argument('--log-stdout', help='show log on stdout, in addition to file',
                        default=False,
                        action='store_true')
    parser.add_argument('--log-debug', help='enable debug level logging',
                    default=False,
                    action='store_true')
    args = parser.parse_args()

    # print ("Args = {}".format(args))

    serve(args)
    
