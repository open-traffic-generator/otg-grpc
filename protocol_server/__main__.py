# Python implementation of gRPC Fake Protocol Server 

#from __future__ import print_function
from concurrent import futures
import argparse
import logging
from pathlib import Path

# snappi
#import snappi

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
OTG_API_Version="0.4.8"

class Openapi(otg_pb2_grpc.OpenapiServicer):

    def __init__(self, args):
        super().__init__()

        self.logger = logging.getLogger(args.logfile)
        #self.app_mode = args.app_mode
        #self.target_address = "{}:{}".format(args.target_host, args.target_port)

        self.api_initialized = False

    def SetConfig(self, request, context):

        jsonObj = json_format.MessageToJson(request.config, including_default_value_fields=True, preserving_proto_field_name=True)
        self.logger.debug("Received request.config (JSON)(default=True) = {}".format(jsonObj))

        jsonObj = json_format.MessageToJson(request.config, preserving_proto_field_name=True)
        self.logger.debug("Received request.config (JSON)(default=True) = {}".format(jsonObj))

        response = """
        {
            "status_code_200" : {
                "success" : {
                    "response_warning" : {
                        "warnings" : ["success message from fake protocol server"]
                    }
                }
            }
        }
        """
        return (json_format.Parse(response, otg_pb2.SetConfigResponse()))

        response = """
        {
            "status_code_400" : {
                "bad_request" : {
                    "response_error" : {
                        "errors" : ["error message from fake protocol server"]
                    }
                }
            }
        }
        """
        return (json_format.Parse(response, otg_pb2.SetConfigResponse()))

        response = """
        {
            "status_code_500" : {
                "internal_server_error" : {
                    "response_error" : {
                        "errors" : ["error message from fake protocol server"]
                    }
                }
            }
        }
        """
        return (json_format.Parse(response, otg_pb2.SetConfigResponse()))


    def SetLinkState(self, request, context):
 
        jsonObj = json_format.MessageToJson(request.link_state, preserving_proto_field_name=True)
        self.logger.debug("Received request.linkstate (JSON) = {}".format(jsonObj))


        response = """
        {
            "status_code_200" : {
                "success" : {
                    "response_warning" : {
                        "warnings" : ["success message from fake protocol server"]
                    }
                }
            }
        }
        """

        return (json_format.Parse(response, otg_pb2.SetLinkStateResponse()))

    def SetTransmitState(self, request, context):
        
        jsonObj = json_format.MessageToJson(request.transmit_state, preserving_proto_field_name=True)
        self.logger.debug("Received request.transmitstate (JSON)(default=False) = {}".format(jsonObj))

        response = """
        {
            "status_code_200" : {
                "success" : {
                    "response_warning" : {
                        "warnings" : ["success message from fake protocol server"]
                    }
                }
            }
        }
        """

        return (json_format.Parse(response, otg_pb2.SetTransmitStateResponse()))


    def GetMetrics(self, request, context):

        jsonObj = json_format.MessageToJson(request.metrics__request, preserving_proto_field_name=True)
        self.logger.debug("Received request.metrics__request (JSON)(default=False) = {}".format(jsonObj))

        response = """
        {
        }
        """
        return json_format.Parse(response.serialize(), otg_pb2.MetricsResponse())


def serve(args):
    log_level = logging.INFO
    if args.log_debug == True:
        log_level = logging.DEBUG
    args.logfile = init_logging(args.logfile, log_level, args.log_stdout)

    server_logger = logging.getLogger(args.logfile) 
    
    server_logger.info("Starting gRPC Server [OTG API Version = {}] ...".format(OTG_API_Version))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    otg_pb2_grpc.add_OpenapiServicer_to_server(Openapi(args), server)
    
    server_address = "[::]:{}".format(args.server_port)

    if args.insecure == True:
        server_logger.info("Enabling insecure channel ...")
        server.add_insecure_port(server_address)
        server_logger.info("Enabled insecure channel")
    else:
        server_logger.info("Enabling secure channel ...")
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
    
    server.start()
    server_logger.info("gRPC Dummy Protocol Server Started at {} ...".format(server_address))

    server.wait_for_termination()
    server_logger.info("Server closed gracefully")



if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-port', help='gRPC server port number',
                        default=40071,
                        type=int)
    parser.add_argument('--logfile', help='logfile name [date and time auto appended]',
                        default='protocol_server',
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
    parser.add_argument('--log-stdout', help='show log on stdout, in addition to file',
                        default=False,
                        action='store_true')
    parser.add_argument('--log-debug', help='enable debug level logging',
                    default=False,
                    action='store_true')
    args = parser.parse_args()

    #print ("Args = {}".format(args))

    serve(args)
