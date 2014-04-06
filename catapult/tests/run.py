""" Test runner for catapult """
import os
import unittest

from catapult.runner import CatapultTestRunner


if __name__ == '__main__':
    # pylint: disable=C0103
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    tests = loader.discover(tests_dir, pattern='*test*.py')
    runner = CatapultTestRunner(format='tap-j')
    runner.run(tests)
