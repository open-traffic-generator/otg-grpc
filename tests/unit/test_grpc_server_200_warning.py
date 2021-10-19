import tests.common.utils as utils


def test_grpc_server_set_config_with_200_warning(snappiserver,
                                                 serverlogfile):
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
            'warnings': [
                'mock 200 set_config warning'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_transmit_state_with_200_warning(snappiserver,
                                                         serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200, True)

    state = {
        "flow_names": [
            "f1"
        ],
        "state": "start"
    }
    json_res = utils.set_transmit_state(grpc_api, state)

    exp_res = {
        'status_code_200': {
            'warnings': [
                'mock 200 set_transmit_state warning'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_link_state_with_200_warning(snappiserver,
                                                     serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200, True)

    state = {
        "port_names": [
            "string"
        ],
        "state": "up"
    }
    json_res = utils.set_link_state(grpc_api, state)

    exp_res = {
        'status_code_200': {
            'warnings': [
                'mock 200 set_link_state warning'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_capture_state_with_200_warning(snappiserver,
                                                        serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200, True)

    state = {
        "port_names": [
            "string"
        ],
        "state": "start"
    }
    json_res = utils.set_capture_state(grpc_api, state)

    exp_res = {
        'status_code_200': {
            'warnings': [
                'mock 200 set_capture_state warning'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_protocol_state_with_200_warning(snappiserver,
                                                         serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200, True)

    state = {
        "state": "start"
    }
    json_res = utils.set_protocol_state(grpc_api, state)

    exp_res = {
        'status_code_200': {
            'warnings': [
                'mock 200 set_protocol_state warning'
            ]
        }
    }
    assert json_res == exp_res


def test_grpc_server_set_route_state_with_200_warning(snappiserver,
                                                      serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 200, True)

    state = {
        "names": [
            "d1"
        ],
        "state": "withdraw"
    }
    json_res = utils.set_route_state(grpc_api, state)

    exp_res = {
        'status_code_200': {
            'warnings': [
                'mock 200 set_route_state warning'
            ]
        }
    }
    assert json_res == exp_res
