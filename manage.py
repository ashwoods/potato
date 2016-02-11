#!/usr/bin/env python
import os
import sys

from tracker.boot import fix_path
fix_path()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")

    from djangae.core.management import execute_from_command_line

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage
        cov = coverage.coverage(source=['tracker'], omit=['*/tests/*'])
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        cov.report()
