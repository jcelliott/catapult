""" Provides the CatapultTestRunner class """
# import time
import sys

from catapult.result import CatapultTestResult


class CatapultTestRunner(object):
    """
    A test runner class that will output results in TAP format
    """

    def __init__(self, stream=sys.stdout, fmt='tap'):
        self.stream = _WritelnDecorator(stream)
        self.result = CatapultTestResult(self.stream, fmt=fmt)

    def run(self, test):
        """ Run the given test case or test suite """
        self.result.startTestRun(test.countTestCases())
        test(self.result)
        self.result.stopTestRun()
        return self.result


class _WritelnDecorator(object):
    """
    Used to decorate file-like objects with a handy 'writeln' method
    From unittest/runner.py
    """
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, arg=None):
        """ write and flush a line of text """
        if arg:
            self.write(arg)
        self.write('\n')  # text-mode streams translate to \r\n if needed
        self.flush()
