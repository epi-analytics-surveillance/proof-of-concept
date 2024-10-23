"""Run software tests.
"""

import argparse
import os
import subprocess
import sys
import unittest


class SoftwareTesting:
    """Methods to run different testing of the software.
    """

    def __init__(self):
        self.test_dir = os.path.join('simsurveillance', 'tests')

    def run_unit_tests(self):
        """Run unit tests.
        """
        tests = unittest.defaultTestLoader.discover(self.test_dir)

        unit_testing = unittest.TextTestRunner().run(tests)

        if not unit_testing.wasSuccessful():
            sys.exit(1)

        return

    def run_flake8(self):
        """Run style check using flake8.
        """
        return subprocess.call(('flake8'))


if __name__ == '__main__':
    testing = SoftwareTesting()

    options = argparse.ArgumentParser(description='Software Testing')
    options.add_argument(
        '--unit', action='store_true', help='Run unit testing')
    options.add_argument(
        '--style', action='store_true', help='Run style check')

    options = options.parse_args()

    if options.unit:
        testing.run_unit_tests()

    if options.style:
        testing.run_flake8()
