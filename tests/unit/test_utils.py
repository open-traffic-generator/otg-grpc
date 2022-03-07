from grpc_server.common.utils import get_error_details


def test_get_error_details():
    exp = Exception("sample error 1")
    status_code, errors = get_error_details(exp)
    assert status_code == 500
    assert errors == [
        'grpc-server - expection arguments is not as expected.',
        'sample error 1'
    ]

    exp = Exception("sample error 1", "sample error 2")
    status_code, errors = get_error_details(exp)
    assert status_code == 500
    assert errors == [
        'grpc-server - 1st argument of exception is not interger type.',
        'sample error 1',
        'grpc-server - 2nd argument of exception is not dict type.',
        'sample error 2'
    ]

    exp = Exception("sample error 1", "sample error 2", "sample error 3")
    status_code, errors = get_error_details(exp)
    assert status_code == 500
    assert errors == [
        'grpc-server - expection arguments is not as expected.',
        'sample error 1',
        'sample error 2',
        'sample error 3'
    ]

    exp = Exception(400, "sample error 1")
    status_code, errors = get_error_details(exp)
    assert status_code == 400
    assert errors == [
        'grpc-server - 2nd argument of exception is not dict type.',
        'sample error 1',
    ]

    exp = Exception(400, {"error": "sample error 1"})
    status_code, errors = get_error_details(exp)
    assert status_code == 400
    assert errors == [
        'grpc-server - errors field is missing in exception',
        "{'error': 'sample error 1'}",
    ]

    exp = Exception(400, {"errors": "sample error 1"})
    status_code, errors = get_error_details(exp)
    assert status_code == 400
    assert errors == [
        'grpc-server - errors field is not a list',
        'sample error 1'
    ]

    exp = Exception(400, {"errors": ["sample error 1"]})
    status_code, errors = get_error_details(exp)
    assert status_code == 400
    assert errors == [
        'sample error 1'
    ]
