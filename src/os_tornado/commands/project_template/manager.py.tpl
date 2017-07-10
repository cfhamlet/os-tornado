#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("OS_TORNADO_SETTINGS_MODULE", "app.settings")
    try:
        from os_tornado.cmdline import execute
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that os-tornado is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import os_tornado
        except ImportError:
            raise ImportError(
                "Couldn't import os-tornado."
                "Are you sure it's installed and "
                "available on your PYTHONPATH environment variable?"
                "Did you forget to activate a virtual environment?"
            )
        raise
    execute(sys.argv)
