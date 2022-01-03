import pytest
import sys
import logging
from grpc_server.common.utils import (get_current_time)
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
    log_file = 'test-'+str(get_current_time())+'.log'
    serverlogfile = init_logging('unit', 'confest', log_file, log_level, False)
    yield serverlogfile
