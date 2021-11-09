import tests.common.utils as utils


def test_grpc_server_set_config_with_200(snappiserver,
                                         serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res


def test_grpc_server_get_config_with_200(snappiserver,
                                         serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

    json_res = utils.get_config(grpc_api)

    exp_res = {
            'status_code_200': {
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
    assert json_res == exp_res


def test_grpc_server_set_transmit_state_with_200(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)

    state = {
        "flow_names": [
            "f1"
        ],
        "state": "start"
    }
    json_res = utils.set_transmit_state(grpc_api, state)

    exp_res = {
        "status_code_200": {}
    }
    assert json_res == exp_res


def test_grpc_server_set_link_state_with_200(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)

    state = {
        "port_names": [
            "string"
        ],
        "state": "up"
    }
    json_res = utils.set_link_state(grpc_api, state)

    exp_res = {
        "status_code_200": {}
    }
    assert json_res == exp_res


def test_grpc_server_get_port_metrics_with_200(snappiserver,
                                               serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

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
        'status_code_200': {
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
    assert json_res == exp_res


def test_grpc_server_get_flow_metrics_with_200(snappiserver,
                                               serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

    metric_req = {
        "choice": "flow",
        "flow": {
            "flow_names": [
                "f1"
            ]
        }
    }

    json_res = utils.get_metrics(grpc_api, metric_req)

    exp_res = {
        'status_code_200': {
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
    assert json_res == exp_res


def test_grpc_server_set_capture_state_with_200(snappiserver,
                                                serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)

    state = {
        "port_names": [
            "string"
        ],
        "state": "start"
    }
    json_res = utils.set_capture_state(grpc_api, state)

    exp_res = {
        "status_code_200": {}
    }
    assert json_res == exp_res


def test_grpc_server_get_capture_with_200(snappiserver,
                                          serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)

    capture_req = {
        "port_name": "rx"
    }
    json_res = utils.get_capture(grpc_api, capture_req)

    exp_res = {
        'status_code_200': 'Ynl0ZXM='
    }
    assert json_res == exp_res


def test_grpc_server_set_protocol_state_with_200(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)

    state = {
        "state": "start"
    }
    json_res = utils.set_protocol_state(grpc_api, state)

    exp_res = {
        "status_code_200": {}
    }
    assert json_res == exp_res


def test_grpc_server_set_route_state_with_200(snappiserver,
                                              serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200)

    state = {
        "names": [
            "d1"
        ],
        "state": "withdraw"
    }
    json_res = utils.set_route_state(grpc_api, state)

    exp_res = {
        "status_code_200": {}
    }
    assert json_res == exp_res


def test_grpc_server_get_ipv4_neighbors_states_with_200(snappiserver,
                                                        serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

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
        'status_code_200': {
            'choice': 'ipv4_neighbors',
            'ipv4_neighbors': [
                {
                    'ethernet_name': 'ipv4_neighbor_eth_1',
                    'ipv4_address': '0.0.0.0',
                    'link_layer_address': '00:00:01:01:01:01'
                }
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_get_ipv6_neighbors_states_with_200(snappiserver,
                                                        serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

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
        'status_code_200': {
            'choice': 'ipv6_neighbors',
            'ipv6_neighbors': [
                {
                    'ethernet_name': 'ipv6_neighbor_eth_1',
                    'ipv6_address': "a:a:a:a:a:a:a:a",
                    'link_layer_address': '00:00:01:01:01:01'
                }
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_send_ipv4_ping_with_200(snappiserver,
                                             serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

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
        'status_code_200': {
            'responses': [
                {
                    'src_name': 'ipv4_1',
                    'dst_ip': '1.1.1.1',
                    'result': 'success'
                }
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_send_ipv6_ping_with_200(snappiserver,
                                             serverlogfile):
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
        "status_code_200": {}
    }
    assert json_res == exp_res

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
        'status_code_200': {
            'responses': [
                {
                    'src_name': 'ipv6_1',
                    'dst_ip': 'a:a:a:a:a:a:a:a',
                    'result': 'success'
                }
            ]
        }
    }
    assert json_res == exp_res
