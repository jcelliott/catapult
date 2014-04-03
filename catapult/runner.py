""" Provides the CatapultTestRunner class """
# import time
import sys
import unittest

from catapult.result import CatapultTestResult
from catapult.formatters import TAPFormatter


class CatapultTestRunner(object):
    """
    A test runner class that will output results in TAP format
    """

    def __init__(self, stream=sys.stdout, buffer=False, format='tap'):
        self.stream = unittest.runner._WritelnDecorator(stream)
        self.result = CatapultTestResult(self.stream, format=format)
        self.result.buffer = buffer

    def run(self, test):
        """ Run the given test case or test suite """
        self.result.startTestRun(test.countTestCases())
        test(self.result)
        self.result.stopTestRun()
        return self.result
