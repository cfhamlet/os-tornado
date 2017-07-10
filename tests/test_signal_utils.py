import signal
import shlex
import sys
import os
import time
import subprocess
from os_tornado.utils.signal_utils import install_shutdown_handlers


_IT_WORKS = 123


def subproc():
    if os.getenv('COVERAGE_PROCESS_START'):
        import coverage
        coverage.process_startup()

    def handler(signum, frame):
        sys.exit(_IT_WORKS)
    install_shutdown_handlers(handler)
    print('start')
    count = 0
    while count < 5:
        time.sleep(1)
        count += 1


def test_install_shutdown_handlers():
    test_env = os.environ.copy()
    if os.getenv('COVERAGE'):
        test_env['COVERAGE_PROCESS_START'] = '.coveragerc'

    proc = subprocess.Popen(shlex.split('python -u %s' %
                                        os.path.abspath(__file__)),
                            stdout=subprocess.PIPE, env=test_env)
    while 'start' not in proc.stdout.readline():
        time.sleep(0.1)
    proc.send_signal(signal.SIGTERM)
    proc.communicate()
    assert _IT_WORKS == proc.returncode


if __name__ == "__main__":
    subproc()
