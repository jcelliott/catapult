""" Provides formatters for TAP, TAP-Y, and TAP-J output"""
TAPYJ_REV = 4


class BaseTAPFormatter(object):

    def __init__(self, stream):
        self.stream = stream


class TAPFormatter(BaseTAPFormatter):

    def __init__(self, stream):
        super(TAPFormatter, self).__init__(stream)

    def suite(self, count, seed=None):
        """ format a suite record """
        self.stream.writeln("1..{}".format(count))
        self.stream.flush()

    def case(self, label, subtype=None, level=0):
        """ format a case record """
        # plain TAP doesn't output case records

    def test(self, test_num, status, label, info=None):
        """ format a test record """
        if status == "pass":
            self.stream.writeln("ok {} - {}".format(test_num, label))
        elif status == "fail" or status == "error":
            self.stream.writeln("not ok {} - {}".format(test_num, label))
        elif status == "omit":
            self.stream.writeln("ok {} # SKIP {}".format(test_num, label))
        self.stream.flush()

    def note(self, text):
        """ format a note record """

    def final(self, counts, tally=False):
        """ format a final or tally record """
        # plain TAP doesn't output anything at the end of a suite


class TAPYFormatter(BaseTAPFormatter):

    def __init__(self, **kwargs):
        super(TAPYFormatter, self).__init__(**kwargs)

    def suite(self, start, count, seed=None):
        """ format a suite record """

    def case(self, label, subtype=None, level=None):
        """ format a case record """

    def test(self, test_num, status, label, info=None):
        """ format a test record """

    def note(self, text):
        """ format a note record """

    def final(self, counts, tally=False):
        """ format a final or tally record """


class TAPJFormatter(BaseTAPFormatter):

    def __init__(self, **kwargs):
        super(TAPJFormatter, self).__init__(**kwargs)

    def suite(self, start, count, seed=None):
        """ format a suite record """

    def case(self, label, subtype=None, level=None):
        """ format a case record """

    def test(self, test_num, status, label, info=None):
        """ format a test record """

    def note(self, text):
        """ format a note record """

    def final(self, counts, tally=False):
        """ format a final or tally record """
