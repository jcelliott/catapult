""" Provides the CatapultTestRunner class """
# import time
import sys
from unittest import TextTestRunner

from catapult.result import CatapultTestResult


class CatapultTestRunner(TextTestRunner):
    """
    A test runner class that will output results in TAP format
    """
    resultclass = CatapultTestResult

    def __init__(self, stream=sys.stdout, **kwargs):
        super(CatapultTestRunner, self).__init__(stream=stream, **kwargs)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        result.before_tests(test)
        test(result)
        return result
