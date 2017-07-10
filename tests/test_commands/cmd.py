import shlex
import os
import sys
import subprocess
from os_tornado.cmdline import execute


def run(cmdline='', env=None, ** kwargs):
    if env is None:
        env = os.environ.copy()
    if env.get('COVERAGE', None) is not None:
        env['COVERAGE_PROCESS_START'] = os.path.abspath('.coveragerc')
    encoding = getattr(sys.stdout, 'encoding') or 'utf-8'
    cmd = 'python -u %s %s' % (os.path.abspath(__file__), cmdline)
    proc = subprocess.Popen(shlex.split(cmd),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env,
                            cwd=os.getcwd(),
                            **kwargs)
    stdout, stderr = proc.communicate()
    return stdout.decode(encoding), stderr.decode(encoding)


if __name__ == "__main__":
    sys.path.insert(0, os.getcwd())
    if os.getenv('COVERAGE_PROCESS_START'):
        import coverage
        coverage.process_startup()
    execute()
