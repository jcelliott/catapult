""" Provides the CatapultTestResult class """
from unittest import result
from catapult.formatters import TAPFormatter, TAPYFormatter, TAPJFormatter


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


class CatapultTestResult(result.TestResult):
    """
    A test result class that outputs TAP
    """

    def __init__(self, stream, fmt='tap', nose=False, include_stdout=True, include_stderr=False):
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
        self.formatter = formatter_class(_WritelnDecorator(stream))
        self.buffer = True
        self.nose = nose
        self.include_stdout = include_stdout
        self.include_stderr = include_stderr

    def startTestRun(self):
        """ Called once before any tests are executed """
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
        current_case = self._get_case_name(test)
        if current_case != self._last_case:
            self.formatter.case(current_case)
            self._last_case = current_case
        super(CatapultTestResult, self).startTest(test)

    def stopTest(self, test):
        # get buffered stdout before calling super.stopTest
        # stdout = self._stdout_buffer.getvalue()
        # stderr = self._stderr_buffer.getvalue()
        super(CatapultTestResult, self).stopTest(test)

    def addSuccess(self, test):
        super(CatapultTestResult, self).addSuccess(test)
        self.formatter.success(self.testsRun,
                               self._get_description(test),
                               self._get_success_info(test))

    def addError(self, test, err):
        super(CatapultTestResult, self).addError(test, err)
        self.formatter.error(self.testsRun,
                             self._get_description(test),
                             self._get_fail_info(test))

    def addFailure(self, test, err):
        super(CatapultTestResult, self).addFailure(test, err)
        self.formatter.fail(self.testsRun,
                            self._get_description(test),
                            self._get_fail_info(test))

    def addSkip(self, test, reason):
        super(CatapultTestResult, self).addSkip(test, reason)
        # just use reason as the label for now
        self.formatter.skip(self.testsRun, reason)

    def addExpectedFailure(self, test, err):
        super(CatapultTestResult, self).addExpectedFailure(test, err)
        # TODO: mark as an expected failure instead of just a pass
        self.formatter.success(self.testsRun,
                               self._get_description(test),
                               self._get_success_info(test))

    def addUnexpectedSuccess(self, test):
        super(CatapultTestResult, self).addUnexpectedSuccess(test)
        # TODO: mark as unexpected success instead of just a fail
        self.formatter.fail(self.testsRun,
                            self._get_description(test),
                            self._get_fail_info(test))

    def _get_success_info(self, test):
        """ generate the info object for a successful test for the formatter class """
        info = {}
        res = self._get_test_result(test)
        if res is not None:
            info['extra'] = {'result': res}
        # TODO: add stdout, stderr
        return info

    def _get_fail_info(self, test):
        """ generate the info object for a failed test for the formatter class """
        # TODO: eventually this needs to be handled differently
        return self._get_success_info(test)

    def _get_test_result(self, test):
        """ try to get the result object from the test """
        if 'result' in test.__dict__:
            return test.result
        return None

    def _get_description(self, test):
        """
        Return the first line of the test's docstring if it exists,
        otherwise return the string representation of the test
        """
        doc_first_line = test.shortDescription()
        if doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def _get_case_name(self, test):
        """ Return the test case name """
        if self.nose:
            # nose wraps the test case in its own test object
            return test.test.__class__.__name__
        else:
            return test.__class__.__name__
