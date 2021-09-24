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
