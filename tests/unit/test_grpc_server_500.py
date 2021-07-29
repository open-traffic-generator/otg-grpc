import pytest
import tests.common.utils as utils


def test_grpc_server_set_config_with_500(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)
    
    config = {
        "ports": [
            {
                "name": "tx",
                "location": "1"
            }
        ]
    }
    json_res = utils.set_config(grpc_api, config)

    exp_res = {
        'status_code_500': {
            'internal_server_error': {
                'response_error': {
                    'errors': [
                        'mock 500 error 1',
                        'mock 500 error 2'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res
    


    

