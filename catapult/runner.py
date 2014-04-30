""" Provides the CatapultTestRunner class """
import sys

from catapult.result import CatapultTestResult


class CatapultTestRunner(object):
    """
    A test runner class that will output results in TAP format
    """

    def __init__(self, stream=sys.stdout, fmt='tap'):
        self.result = CatapultTestResult(stream, fmt=fmt)

    def run(self, test):
        """ Run the given test case or test suite """
        self.result.total_tests = test.countTestCases()
        self.result.startTestRun()
        test(self.result)
        self.result.stopTestRun()
        return self.result
