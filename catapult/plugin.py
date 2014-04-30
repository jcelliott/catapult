""" The plugin module provides a nose test plugin for catapult """
import os

from nose.plugins import Plugin

from catapult.runner import CatapultTestRunner


class CatapultPlugin(Plugin):
    """
    A nose plugin that produces test results in TAP, TAP-J, and TAP-Y formats
    """
    name = 'catapult'
    score = 2000

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
        options.logcapture = True

    def prepareTestRunner(self, runner):  # pylint: disable=C0103
        """ Replace the test runner with catapult's runner """
        return CatapultTestRunner(stream=runner.stream,
                                  fmt=self.conf.options.catapult_format)

    def prepareTestResult(self, result):  # pylint: disable=C0103
        """ Configure catapult's test result class """
        result.nose = True
        result.include_stdout = self.conf.options.catapult_stdout
        result.include_stderr = self.conf.options.catapult_stderr
