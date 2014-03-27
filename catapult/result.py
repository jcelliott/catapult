""" Provides the CatapultTestResult class """
from unittest import result
import time


class CatapultTestResult(result.TestResult):
    """
    A test result class that outputs TAP
    """

    def __init__(self, stream, descriptions, verbosity):
        super(CatapultTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.dots = verbosity == 1
        self.descriptions = descriptions
        self.start_time = None

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

    def startTestRun(self):
        """ Called once before any tests are executed """

    def stopTestRun(self):
        """ Called once after all tests are executed """

    def before_tests(self, suite):
        """ Called with the entire test suite before any tests are run """
        self.stream.writeln("1..{}".format(suite.countTestCases()))
        self.start_time = time.time()

    def startTest(self, test):
        super(CatapultTestResult, self).startTest(test)

    def stopTest(self, test):
        super(CatapultTestResult, self).stopTest(test)

    def addSuccess(self, test):
        super(CatapultTestResult, self).addSuccess(test)
        self.stream.writeln("ok {} - {}".format(self.testsRun, self.get_description(test)))

    def addError(self, test, err):
        super(CatapultTestResult, self).addError(test, err)
        self.stream.writeln("not ok {} - {}".format(self.testsRun, self.get_description(test)))

    def addFailure(self, test, err):
        super(CatapultTestResult, self).addFailure(test, err)
        self.stream.writeln("not ok {} - {}".format(self.testsRun, self.get_description(test)))

    def addSkip(self, test, reason):
        super(CatapultTestResult, self).addSkip(test, reason)
        self.stream.writeln("ok {} # skipped {}".format(self.testsRun, reason))

    def addExpectedFailure(self, test, err):
        super(CatapultTestResult, self).addExpectedFailure(test, err)
        self.stream.writeln("not ok {} - expected failure for: {}"
                            .format(self.testsRun, self.get_description(test)))

    def addUnexpectedSuccess(self, test):
        super(CatapultTestResult, self).addUnexpectedSuccess(test)
        self.stream.writeln("not ok {} - unexpected success for: {}"
                            .format(self.testsRun, self.get_description(test)))

    # def printErrors(self):
        # if self.dots or self.showAll:
        #     self.stream.writeln()
        # self.printErrorList('ERROR', self.errors)
        # self.printErrorList('FAIL', self.failures)

    # def printErrorList(self, flavour, errors):
        # for test, err in errors:
        #     self.stream.writeln(self.separator1)
        #     self.stream.writeln("%s: %s" % (flavour,self.get_description(test)))
        #     self.stream.writeln(self.separator2)
        #     self.stream.writeln("%s" % err)
