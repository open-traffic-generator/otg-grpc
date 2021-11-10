import tests.common.utils as utils


def test_grpc_server_set_config_with_400(snappiserver,
                                         serverlogfile):
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
            'errors': [
                'mock 400 set_config error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_config_with_400(snappiserver,
                                         serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    json_res = utils.get_config(grpc_api)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 get_config error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_transmit_state_with_400(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    state = {
        "flow_names": [
            "f1"
        ],
        "state": "start"
    }
    json_res = utils.set_transmit_state(grpc_api, state)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 set_transmit_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_link_state_with_400(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    state = {
        "port_names": [
            "string"
        ],
        "state": "up"
    }
    json_res = utils.set_link_state(grpc_api, state)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 set_link_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_port_metrics_with_400(snappiserver,
                                               serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    metric_req = {
        "choice": "port",
        "port": {
            "port_names": [
                "tx"
            ]
        }
    }

    json_res = utils.get_metrics(grpc_api, metric_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 get_metrics error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_set_capture_state_with_400(snappiserver,
                                                serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    state = {
        "port_names": [
            "string"
        ],
        "state": "start"
    }
    json_res = utils.set_capture_state(grpc_api, state)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 set_capture_state error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_get_capture_with_400(snappiserver,
                                          serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    capture_req = {
        "port_name": "rx"
    }
    json_res = utils.get_capture(grpc_api, capture_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 get_capture error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_set_protocol_state_with_400(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    state = {
        "state": "start"
    }
    json_res = utils.set_protocol_state(grpc_api, state)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 set_protocol_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_route_state_with_400(snappiserver,
                                              serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    state = {
        "names": [
            "d1"
        ],
        "state": "withdraw"
    }
    json_res = utils.set_route_state(grpc_api, state)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 set_route_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_ipv4_neighbors_states_with_400(snappiserver,
                                                        serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    states_req = {
        "choice": "ipv4_neighbors",
        "ipv4_neighbors": {
            "ethernet_names": [
                "ipv4_neighbor_eth_1"
            ]
        }
    }

    json_res = utils.get_states(grpc_api, states_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 get_states error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_get_ipv6_neighbors_states_with_400(snappiserver,
                                                        serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    states_req = {
        "choice": "ipv6_neighbors",
        "ipv6_neighbors": {
            "ethernet_names": [
                "ipv6_neighbor_eth_1"
            ]
        }
    }

    json_res = utils.get_states(grpc_api, states_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 get_states error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_send_ipv4_ping_with_400(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    ping_req = {
        "endpoints": [
            {
                "choice": "ipv4",
                "ipv4": {
                    "src_name": "ipv4_1",
                    "dst_ip": "1.1.1.1"
                }
            }
        ],
    }

    json_res = utils.send_ping(grpc_api, ping_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 send_ping error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_send_ipv6_ping_with_400(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    ping_req = {
        "endpoints": [
            {
                "choice": "ipv6",
                "ipv6": {
                    "src_name": "ipv6_1",
                    "dst_ip": "a:a:a:a:a:a:a:a"
                }
            }
        ],
    }

    json_res = utils.send_ping(grpc_api, ping_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 send_ping error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_update_flows_with_400(snappiserver,
                                           serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 400)

    update_flow_req = {
        "property_names": [
            "rate",
            "size"
        ],
        "flows": [
            {
                "name": "f1",
                "tx_rx": {
                    "choice": "port",
                    "port": {
                        "tx_name": "tx",
                        "rx_name": "rx"
                    }
                },
                "metrics": {
                    "enable": True
                },
                "size": {
                    "choice": "fixed",
                    "fixed": 512
                },
                "rate": {
                    "choice": "percentage",
                    "percentage": 50
                },
                "duration": {
                    "choice": "fixed_packets",
                    "fixed_packets": {
                        "packets": 110
                    }
                },
                "packet": [
                    {
                        "choice": "ethernet",
                        "ethernet": {
                            "dst": {
                                "choice": "value",
                                "value": "00:AB:BC:AB:BC:AB"
                            },
                            "src": {
                                "choice": "value",
                                "value": "00:CD:DC:CD:DC:CD"
                            }
                        }
                    }
                ]
            }
        ]
    }

    json_res = utils.update_flows(grpc_api, update_flow_req)

    exp_res = {
        'status_code_400': {
            'errors': [
                'mock 400 update_flows error'
                ]
            }
        }
    assert json_res == exp_res
