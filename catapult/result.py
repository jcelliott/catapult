""" Provides the CatapultTestResult class """
from unittest import result
import time
from catapult.formatters import TAPFormatter, TAPYFormatter, TAPJFormatter


class CatapultTestResult(result.TestResult):
    """
    A test result class that outputs TAP
    """

    def __init__(self, stream, format='tap'):
        super(CatapultTestResult, self).__init__()
        self.start_time = None
        self._last_case = None
        self.total_tests = 0
        format = format.lower()
        if format == 'tap-j' or format == 'tapj':
            formatter_class = TAPJFormatter
        elif format == 'tap-y' or format == 'tapy':
            formatter_class = TAPYFormatter
        else:
            formatter_class = TAPFormatter
        self.formatter = formatter_class(stream)

    def get_description(self, test):
        """
        Return the first line of the test's docstring if it exists,
        otherwise return the string representation of the test
        """
        doc_first_line = test.shortDescription()
        if doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def startTestRun(self, total_tests=None):
        """ Called once before any tests are executed """
        if total_tests is not None:
            self.total_tests = total_tests
        self.formatter.suite(self.total_tests)

    def stopTestRun(self):
        """ Called once after all tests are executed """
        num_fail = len(self.failures) + len(self.unexpectedSuccesses)
        num_pass = self.testsRun - num_fail - len(self.errors)
        counts = {
            'total': self.testsRun,
            'pass': num_pass,
            'fail': num_fail,
            'error': len(self.errors),
            'omit': len(self.skipped),
            'todo': 0,
        }
        self.formatter.final(counts)

    def startTest(self, test):
        if test.__class__ != self._last_case:
            self.formatter.case(test.__class__.__name__)
            self._last_case = test.__class__
        super(CatapultTestResult, self).startTest(test)

    def stopTest(self, test):
        super(CatapultTestResult, self).stopTest(test)

    def addSuccess(self, test):
        super(CatapultTestResult, self).addSuccess(test)
        self.formatter.test(self.testsRun, 'pass', self.get_description(test))

    def addError(self, test, err):
        super(CatapultTestResult, self).addError(test, err)
        self.formatter.test(self.testsRun, 'error', self.get_description(test))

    def addFailure(self, test, err):
        super(CatapultTestResult, self).addFailure(test, err)
        self.formatter.test(self.testsRun, 'fail', self.get_description(test))

    def addSkip(self, test, reason):
        super(CatapultTestResult, self).addSkip(test, reason)
        # just use reason as the label for now
        self.formatter.test(self.testsRun, 'omit', reason)

    def addExpectedFailure(self, test, err):
        super(CatapultTestResult, self).addExpectedFailure(test, err)
        # TODO: mark as an expected failure instead of just a pass
        self.formatter.test(self.testsRun, 'pass', self.get_description(test))

    def addUnexpectedSuccess(self, test):
        super(CatapultTestResult, self).addUnexpectedSuccess(test)
        # TODO: mark as unexpected success instead of just a fail
        self.formatter.test(self.testsRun, 'fail', self.get_description(test))
