import tests.common.utils as utils


def test_grpc_server_set_config_with_501(snappiserver,
                                         serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    config = {
        "ports": [
            {
                "name": "tx",
                "location": "1"
            }
        ]
    }

    found_err = False
    try:
        utils.set_config(grpc_api, config)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_get_config_with_501(snappiserver,
                                         serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    found_err = False
    try:
        utils.get_config(grpc_api)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_set_transmit_state_with_501(snappiserver,
                                                 serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    state = {
        "flow_names": [
            "f1"
        ],
        "state": "start"
    }

    found_err = False
    try:
        utils.set_transmit_state(grpc_api, state)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_set_link_state_with_501(snappiserver,
                                             serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    state = {
        "port_names": [
            "string"
        ],
        "state": "up"
    }

    found_err = False
    try:
        utils.set_link_state(grpc_api, state)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_get_metrics_with_501(snappiserver,
                                          serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    metrc_req = {
        "choice": "flow",
        "flow": {
            "flow_names": [
                "f1"
            ]
        }
    }

    found_err = False
    try:
        utils.get_metrics(grpc_api, metrc_req)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_get_port_metrics_with_501(snappiserver,
                                               serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    metric_req = {
        "choice": "port",
        "port": {
            "port_names": [
                "tx"
            ]
        }
    }

    found_err = False
    try:
        utils.get_metrics(grpc_api, metric_req)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_set_capture_state_with_501(snappiserver,
                                                serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    state = {
        "port_names": [
            "string"
        ],
        "state": "start"
    }

    found_err = False
    try:
        utils.set_capture_state(grpc_api, state)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'


def test_grpc_server_get_capture_with_501(snappiserver,
                                          serverlogfile):
    grpc_api = utils.init_grpc_with_mock_server(serverlogfile, 501)

    capture_req = {
        "port_name": "rx"
    }

    found_err = False
    try:
        utils.get_capture(grpc_api, capture_req)
    except Exception:
        found_err = True

    assert found_err, 'Exception should be raised'
