import pytest
import tests.common.utils as utils


def test_grpc_server_set_config_with_200_warning(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200, True)
    
    config = {
        "ports": [
            {
                "name": "tx",
                "location": "localhost:5555"
            }
        ]
    }
    json_res = utils.set_config(grpc_api, config)

    exp_res = {
        'status_code_200': {
            'success': {
                'response_warning': {
                    'warnings': [
                        'mock warning 1',
                        'mock warning 2'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res

