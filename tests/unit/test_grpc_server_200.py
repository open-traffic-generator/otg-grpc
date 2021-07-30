import pytest
import tests.common.utils as utils


def test_grpc_server_set_config_with_200(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)
    
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
        "status_code_200": {
            "success": {
            "response_warning": {}
            }
        }
    }
    assert json_res == exp_res

def test_grpc_server_get_config_with_200(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)
    
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
        "status_code_200": {
            "success": {
            "response_warning": {}
            }
        }
    }
    assert json_res == exp_res

    json_res = utils.get_config(grpc_api)

    exp_res = {
            'status_code_200': {
                'config': {
                    'ports': [
                        {
                            'location': 'localhost:5555', 
                            'name': 'tx'
                        }
                    ], 
                'options': {
                    'port_options': {
                        'location_preemption': False
                    }
                }
            }
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_transmit_state_with_200(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)
    
    state = {
        "flow_names": [
            "f1"
        ],
        "state" : "start"
    }
    json_res = utils.set_transmit_state(grpc_api, state)

    exp_res = {
        "status_code_200": {
            "success": {
            "response_warning": {}
            }
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_link_state_with_200(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)
    
    state = {
        "port_names": [
            "string"
        ],
        "state": "up"
    }
    json_res = utils.set_link_state(grpc_api, state)

    exp_res = {
        "status_code_200": {
            "success": {
            "response_warning": {}
            }
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_port_metrics_with_200(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)
    
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
        "status_code_200": {
            "success": {
            "response_warning": {}
            }
        }
    }
    assert json_res == exp_res

    metrc_req = {
        "choice": "port",
        "port": {
            "port_names": [
                "tx"
            ]
        }
    }

    json_res = utils.get_metrics(grpc_api, metrc_req)

    exp_res = {
        'status_code_200': {
            'metrics_response': {
                'choice': 'port_metrics',
                'port_metrics': [
                    {
                        'name': 'tx',
                        'frames_tx': 10000,
                        'frames_rx': 10000
                    }
                ]
            }
        }
    }
    assert json_res == exp_res

def test_grpc_server_get_flow_metrics_with_200(snappiserver, serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)
    
    config = {
        "ports": [
            {
                "name": "tx",
                "location": "localhost:5555"
            }
        ],
        "flows": [
            {
                "name": "f1",
                "tx_rx": {
                    "choice": "port",
                    "port": {
                        "tx_name": "tx"
                    }
                }
            }
        ]
    }
    json_res = utils.set_config(grpc_api, config)

    exp_res = {
        "status_code_200": {
            "success": {
            "response_warning": {}
            }
        }
    }
    assert json_res == exp_res

    metrc_req = {
        "choice": "flow",
        "flow": {
            "flow_names": [
                "f1"
            ]
        }
    }

    json_res = utils.get_metrics(grpc_api, metrc_req)

    exp_res = {
        'status_code_200': {
            'metrics_response': {
                'choice': 'flow_metrics',
                'flow_metrics': [
                    {
                        'name': 'f1',
                        'frames_tx': 10000,
                        'frames_rx': 10000
                    }
                ]
            }
        }
    }
    assert json_res == exp_res


