import pytest
import sys
import logging
sys.path.append('.')


@pytest.fixture(scope='session')
def snappiserver():
    """Demonstrates creating Mock Snappi Servers.
    """
    from .snappiserver import SnappiServer
    pytest.snappiserver = SnappiServer().start()

    yield


@pytest.fixture(scope='session')
def serverlogfile():
    """Demonstrates creating server log file
    """
    from grpc_server.common.utils import init_logging
    log_level = logging.INFO
    serverlogfile = init_logging('test', log_level, False)
    yield serverlogfile
