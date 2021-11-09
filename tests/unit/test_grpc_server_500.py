import tests.common.utils as utils


def test_grpc_server_set_config_with_500(snappiserver,
                                         serverlogfile):
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
            'errors': [
                'mock 500 set_config error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_config_with_500(snappiserver,
                                         serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    json_res = utils.get_config(grpc_api)

    exp_res = {
        'status_code_500': {
            'errors': [
                'mock 500 get_config error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_transmit_state_with_500(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    state = {
        "flow_names": [
            "f1"
        ],
        "state": "start"
    }
    json_res = utils.set_transmit_state(grpc_api, state)

    exp_res = exp_res = {
        'status_code_500': {
            'errors': [
                'mock 500 set_transmit_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_link_state_with_500(snappiserver,
                                             serverlogfile):
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
            'errors': [
                'mock 500 set_link_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_port_metrics_with_500(snappiserver,
                                               serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

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
        'status_code_500': {
            'errors': [
                'mock 500 get_metrics error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_set_capture_state_with_500(snappiserver,
                                                serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    state = {
        "port_names": [
            "string"
        ],
        "state": "start"
    }
    json_res = utils.set_capture_state(grpc_api, state)

    exp_res = {
        'status_code_500': {
            'errors': [
                'mock 500 set_capture_state error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_get_capture_with_500(snappiserver,
                                          serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    capture_req = {
        "port_name": "rx"
    }
    json_res = utils.get_capture(grpc_api, capture_req)

    exp_res = {
        'status_code_500': {
            'errors': [
                'mock 500 get_capture error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_set_protocol_state_with_500(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    state = {
        "state": "start"
    }
    json_res = utils.set_protocol_state(grpc_api, state)

    exp_res = exp_res = {
        'status_code_500': {
            'errors': [
                'mock 500 set_protocol_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_route_state_with_500(snappiserver,
                                              serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

    state = {
        "names": [
            "d1"
        ],
        "state": "withdraw"
    }
    json_res = utils.set_route_state(grpc_api, state)

    exp_res = exp_res = {
        'status_code_500': {
            'errors': [
                'mock 500 set_route_state error'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_ipv4_neighbors_states_with_500(snappiserver,
                                                        serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

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
        'status_code_500': {
            'errors': [
                'mock 500 get_states error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_get_ipv6_neighbors_states_with_500(snappiserver,
                                                        serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

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
        'status_code_500': {
            'errors': [
                'mock 500 get_states error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_send_ipv4_ping_with_500(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

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
        'status_code_500': {
            'errors': [
                'mock 500 send_ping error'
                ]
            }
        }
    assert json_res == exp_res


def test_grpc_server_send_ipv6_ping_with_500(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 500)

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
        'status_code_500': {
            'errors': [
                'mock 500 send_ping error'
                ]
            }
        }
    assert json_res == exp_res
