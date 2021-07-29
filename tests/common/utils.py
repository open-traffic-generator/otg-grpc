import argparse
import os
import json
from google.protobuf import json_format

from grpc_server.__main__ import Openapi
from grpc_server.autogen import otg_pb2


SETTINGS_FILE = 'settings.json'
TESTS_FOLDER = 'tests'
MOCK_GRPC_SERVER_CONTEXT = "test"


def get_root_dir():
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )


def get_settings_file_path():
    tests_dir = get_root_dir()
    if not tests_dir.endswith(TESTS_FOLDER):
        tests_dir = os.path.join(tests_dir, TESTS_FOLDER)
    return os.path.join(tests_dir, SETTINGS_FILE)


def convert_proto_to_json(proto_obj):
    json_obj = json.loads(
        json_format.MessageToJson(
            proto_obj,
            including_default_value_fields=False,
            preserving_proto_field_name=True
        )
    )

    return json_obj



def get_parsed_args(op_val):
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-port', help='gRPC server port number',
                        default=40051,
                        type=int)
    parser.add_argument('--app-mode', help='target Application mode)',
                        choices=['ixnetwork', 'athena', 'athena-insecure'],
                        default='ixnetwork',
                        type=str)
    parser.add_argument('--target-host', help='target host address',
                        default='localhost',
                        type=str)
    parser.add_argument('--target-port', help='target port number',
                        default=11009,
                        type=int)
    parser.add_argument('--logfile', help='logfile name [date and time auto appended]',
                        default='grpc_server',
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

    arg_inputs = []
    for op, val in list(op_val.items()):
        arg_inputs.append('--{}'.format(op))
        arg_inputs.append('{}'.format(val))

    args = parser.parse_args(arg_inputs)
    return args


def get_mock_server_settings(error_code=200, with_warning=False):
    file_path = get_settings_file_path()
    with open(file_path, 'r') as fp:
        ut_settings = json.load(fp)

    port_type = "{}".format(error_code)
    if with_warning:
        port_type += "-warning"

    mock_config = {
        "app-mode": ut_settings["app-mode"],
        "target-host": ut_settings["target-host"],
        "target-port": ut_settings["target-port"][port_type]
    }

    return mock_config



def init_grpc_with_mock_server(server_logfile, error_code=200, with_warning=False):
    print('Intializing grpc server api......')
    mock_config = get_mock_server_settings(error_code, with_warning)
    mock_config['logfile'] = server_logfile
    mock_config_args = get_parsed_args(mock_config)
    grpc_api = Openapi(mock_config_args)
    return grpc_api


def set_config(api, payload):
    print('Setting Config......')
    if not isinstance(payload, str):
        # accept both string and dict
        payload = json.dumps(payload, indent=4)
    proto_config_req = json_format.Parse(payload, otg_pb2.Config())
    req_obj = otg_pb2.SetConfigRequest(config=proto_config_req)
    proto_res = api.SetConfig(req_obj, MOCK_GRPC_SERVER_CONTEXT)
    json_res = convert_proto_to_json(proto_res)
    return json_res


def get_config(api):
    print('Getting Config......')
    empty_req_obj = otg_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    proto_res = api.GetConfig(empty_req_obj, MOCK_GRPC_SERVER_CONTEXT)
    json_res = convert_proto_to_json(proto_res)
    return json_res


def set_transmit_state(api, payload):
    print('Setting Transmit State......')
    if not isinstance(payload, str):
        # accept both string and dict
        payload = json.dumps(payload, indent=4)
    proto_state_req = json_format.Parse(payload, otg_pb2.TransmitState())
    req_obj = otg_pb2.SetTransmitStateRequest(transmit_state=proto_state_req)
    proto_res = api.SetTransmitState(req_obj, MOCK_GRPC_SERVER_CONTEXT)
    json_res = convert_proto_to_json(proto_res)
    return json_res

def set_link_state(api, payload):
    print('Setting Link State......')
    if not isinstance(payload, str):
        # accept both string and dict
        payload = json.dumps(payload, indent=4)
    proto_state_req = json_format.Parse(payload, otg_pb2.LinkState())
    req_obj = otg_pb2.SetLinkStateRequest(link_state=proto_state_req)
    proto_res = api.SetLinkState(req_obj, MOCK_GRPC_SERVER_CONTEXT)
    json_res = convert_proto_to_json(proto_res)
    return json_res

def get_metrics(api, payload):
    print('Fetching Metrices......')
    if not isinstance(payload, str):
        # accept both string and dict
        payload = json.dumps(payload, indent=4)
    proto_state_req = json_format.Parse(payload, otg_pb2.MetricsRequest())
    req_obj = otg_pb2.GetMetricsRequest(metrics_request=proto_state_req)
    proto_res = api.GetMetrics(req_obj, MOCK_GRPC_SERVER_CONTEXT)
    json_res = convert_proto_to_json(proto_res)
    return json_res




