""" Provides the CatapultTestResult class """
from unittest import result
from catapult.formatters import TAPFormatter, TAPYFormatter, TAPJFormatter


class CatapultTestResult(result.TestResult):
    """
    A test result class that outputs TAP
    """

    def __init__(self, stream, fmt='tap'):
        super(CatapultTestResult, self).__init__()
        self.start_time = None
        self._last_case = None
        self.total_tests = 0
        fmt = fmt.lower()
        if fmt == 'tap-j' or fmt == 'tapj':
            formatter_class = TAPJFormatter
        elif fmt == 'tap-y' or fmt == 'tapy':
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

    def startTestRun(self, total_tests=None):  # pylint: disable=W0221
        """ Called once before any tests are executed """
        if total_tests is not None:
            self.total_tests = total_tests
        self.formatter.suite(self.total_tests)

    def stopTestRun(self):
        """ Called once after all tests are executed """
        num_fail = len(self.failures) + len(self.unexpectedSuccesses)
        num_pass = self.testsRun - num_fail - len(self.errors) - len(self.skipped)
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
        self.formatter.success(self.testsRun,
                               self.get_description(test),
                               self._get_success_info(test))

    def addError(self, test, err):
        super(CatapultTestResult, self).addError(test, err)
        self.formatter.error(self.testsRun,
                             self.get_description(test),
                             self._get_fail_info(test))

    def addFailure(self, test, err):
        super(CatapultTestResult, self).addFailure(test, err)
        self.formatter.fail(self.testsRun,
                            self.get_description(test),
                            self._get_fail_info(test))

    def addSkip(self, test, reason):
        super(CatapultTestResult, self).addSkip(test, reason)
        # just use reason as the label for now
        self.formatter.skip(self.testsRun, reason)

    def addExpectedFailure(self, test, err):
        super(CatapultTestResult, self).addExpectedFailure(test, err)
        # TODO: mark as an expected failure instead of just a pass
        self.formatter.success(self.testsRun,
                               self.get_description(test),
                               self._get_success_info(test))

    def addUnexpectedSuccess(self, test):
        super(CatapultTestResult, self).addUnexpectedSuccess(test)
        # TODO: mark as unexpected success instead of just a fail
        self.formatter.fail(self.testsRun,
                            self.get_description(test),
                            self._get_fail_info(test))

    def _get_success_info(self, test):
        """ generate the info object for a successful test for the formatter class """
        res = self._get_test_result(test)
        if res is not None:
            return {'extra': {'result': res}}
        return None

    def _get_fail_info(self, test):
        """ generate the info object for a failed test for the formatter class """
        # TODO: eventually this needs to be handled differently
        return self._get_success_info(test)

    def _get_test_result(self, test):
        """ try to get the result object from the test """
        if 'result' in test.__dict__:
            return test.result
        return None
