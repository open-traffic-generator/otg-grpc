import pytest
import tests.common.utils as utils


def test_grpc_server_set_config_with_400(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)
    
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
        'status_code_400': {
            'bad_request': {
                'response_error': {
                    'errors': [
                        'mock 400 error 1',
                        'mock 400 error 2'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res
    


    

