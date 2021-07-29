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
                        'mock 500 set_config error'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_config_with_500(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    json_res = utils.get_config(grpc_api)

    exp_res = {
        'status_code_500': {
            'internal_server_error': {
                'response_error': {
                    'errors': [
                        'mock 500 get_config error'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_transmit_state_with_500(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)
    
    state = {
        "flow_names": [
            "f1"
        ],
        "state" : "start"
    }
    json_res = utils.set_transmit_state(grpc_api, state)

    exp_res = exp_res = {
        'status_code_500': {
            'internal_server_error': {
                'response_error': {
                    'errors': [
                        'mock 500 set_transmit_state error'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_link_state_with_500(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)
    
    state = {
        "port_names": [
            "string"
        ],
        "state": "up"
    }
    json_res = utils.set_link_state(grpc_api, state)

    exp_res = exp_res = {
        'status_code_500': {
            'internal_server_error': {
                'response_error': {
                    'errors': [
                        'mock 500 set_link_state error'
                    ]
                }
            }
        }
    }
    assert json_res == exp_res
    


    

