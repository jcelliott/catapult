""" The plugin module provides a nose test plugin for catapult """
import os
import sys
from StringIO import StringIO

from nose.plugins import Plugin

from catapult.result import CatapultTestResult


class CatapultPlugin(Plugin):
    """
    A nose plugin that produces test results in TAP, TAP-J, and TAP-Y formats
    """
    name = 'catapult'
    score = 2000

    def __init__(self, *args, **kwargs):
        super(CatapultPlugin, self).__init__(*args, **kwargs)
        self.result = None
        self.test_suite = None
        self.stream = sys.stdout
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def options(self, parser, env=os.environ):  # pylint: disable=W0102
        super(CatapultPlugin, self).options(parser, env=env)
        parser.add_option('--catapult-format',
                          type='string',
                          dest='catapult_format',
                          default=env.get('CATAPULT_FORMAT', 'tap-j'),
                          help="The output format for the test results. "
                               "Options are 'tap', 'tap-j' and 'tap-y'.")
        parser.add_option('--catapult-stdout',
                          action='store_true',
                          dest='catapult_stdout',
                          default=True,
                          help="Include stdout from tests in catapult results")
        parser.add_option('--catapult-no-stdout',
                          action='store_false',
                          dest='catapult_stdout',
                          help="Don't include stdout from tests in catapult results")
        parser.add_option('--catapult-stderr',
                          action='store_true',
                          dest='catapult_stderr',
                          default=False,
                          help="Include stderr from tests in catapult results")
        parser.add_option('--catapult-no-stderr',
                          action='store_false',
                          dest='catapult_stderr',
                          help="Don't include stderr from tests in catapult results")

    def configure(self, options, conf):
        super(CatapultPlugin, self).configure(options, conf)
        if not self.enabled:
            return
        options.capture = False
        # TODO: how to handle logs?
        options.logcapture = False

    def prepareTest(self, test):
        """ Called with the entire test suite before starting the test """
        # cache the test suite so `prepareTestResult` can use it later
        self.test_suite = test

    def finalize(self, _):
        """ Print final test results (TAP-Y/J 'final' record) """
        self.result.stopTestRun()

    def setOutputStream(self, stream):
        """ Capture the output stream so only catapult can use it """
        self.stream = stream
        # self.runner.stream = stream
        class FakeStream:
            def write(self, *arg):
                pass
            def writeln(self, *arg):
                pass
        fake_stream = FakeStream()
        return fake_stream

    def prepareTestResult(self, result):
        """ Configure catapult's test result class """
        # pass in the captured stream
        self.result = CatapultTestResult(self.stream,
                                         nose=True,
                                         fmt=self.conf.options.catapult_format)
        # result.include_stdout = self.conf.options.catapult_stdout
        # result.include_stderr = self.conf.options.catapult_stderr

        # start the TAP output (see CatapultTestRunner)
        self.result.total_tests = self.test_suite.countTestCases()
        self.result.startTestRun()
        return self.result
