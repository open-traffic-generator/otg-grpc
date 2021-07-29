import pytest
import sys
import subprocess
import time
import logging
sys.path.append('.')

@pytest.fixture(scope='session')
def snappiserver():
    """Demonstrates creating Mock Snappi Servers.
    """
    from .mocksnappiservers.snappiserver200 import SnappiServer200
    pytest.snappiserver200 = SnappiServer200().start()

    from .mocksnappiservers.snappiserver200warning import SnappiServer200Warning
    pytest.snappiserver200warning = SnappiServer200Warning().start()

    from .mocksnappiservers.snappiserver400 import SnappiServer400
    pytest.snappiserver400 = SnappiServer400().start()

    from .mocksnappiservers.snappiserver500 import SnappiServer500
    pytest.snappiserver500 = SnappiServer500().start()
    yield

@pytest.fixture(scope='session')
def serverlogfile():
    """Demonstrates creating server log file
    """
    from grpc_server.common.utils import init_logging
    log_level = logging.INFO
    serverlogfile = init_logging('test', log_level, False)
    yield serverlogfile

