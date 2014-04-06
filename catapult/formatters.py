""" Provides formatters for TAP, TAP-Y, and TAP-J output"""
# pylint: disable=W0613
from datetime import datetime
import json
import yaml

TAPYJ_REV = 4


class BaseTAPFormatter(object):
    """ Common functionality for all formatter classes """

    def __init__(self, stream):
        self.stream = stream
        self.start_time = datetime.now()

    def elapsed_time(self):
        """ Return the number of seconds since the test started """
        return (datetime.now() - self.start_time).total_seconds()


class TAPFormatter(BaseTAPFormatter):
    """ Format test results in plain TAP format """

    def __init__(self, stream):
        super(TAPFormatter, self).__init__(stream)

    def suite(self, count, seed=None):
        """ format a suite record """
        self.stream.writeln("1..{}".format(count))

    def case(self, label, subtype=None, level=0):
        """ format a case record """
        # plain TAP doesn't output case records

    def success(self, test_num, label, info=None):
        """ format a test record with status 'pass' """
        self.stream.writeln("ok {} - {}".format(test_num, label))

    def fail(self, test_num, label, info=None):
        """ format a test record with status 'fail' """
        self.stream.writeln("not ok {} - {}".format(test_num, label))

    def error(self, test_num, label, info=None):
        """ format a test record with status 'error' """
        self.stream.writeln("not ok {} - {}".format(test_num, label))

    def skip(self, test_num, label, info=None):
        """ format a test record with status 'omit' """
        self.stream.writeln("ok {} # SKIP {}".format(test_num, label))

    def todo(self, test_num, label, info=None):
        """ format a test record with status 'todo' """
        self.stream.writeln("not ok {} # TODO {}".format(test_num, label))  # pylint: disable=W0511

    def note(self, text):
        """ format a note record """

    def final(self, counts, tally=False):
        """ format a final or tally record """
        # plain TAP doesn't output anything at the end of a suite


class SerializingTAPFormatter(BaseTAPFormatter):
    """ Common functionality for formatters that use a serialize function (TAP-Y and TAP-J) """

    def __init__(self, stream):
        super(SerializingTAPFormatter, self).__init__(stream)

    def serialize(self, data, final=False):
        """ serialize a test record """
        raise NotImplementedError("Subclasses must implement their own serialize method")

    def suite(self, count, seed=None):
        """ format a suite record """
        suite = {
            'type': 'suite',
            'start': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count,
            'rev': TAPYJ_REV,
        }
        if seed is not None:
            suite['seed'] = seed

        # compact encoding?
        self.stream.writeln(self.serialize(suite))

    def case(self, label, subtype=None, level=0):
        """ format a case record """
        case = {
            'type': 'case',
            'label': label,
            'level': level,
        }
        if subtype is not None:
            case['subtype'] = subtype
        self.stream.writeln(self.serialize(case))

    def test(self, status, label):
        """ format a test record """
        test = {
            'type': 'test',
            'status': status,
            'time': self.elapsed_time(),
            'label': label,
        }
        return test

    def success(self, test_num, label, info=None):
        """ format a test record with status 'pass' """
        test = self.test('pass', label)
        self.stream.writeln(self.serialize(test))

    def fail(self, test_num, label, info=None):
        """ format a test record with status 'fail' """
        test = self.test('fail', label)
        self.stream.writeln(self.serialize(test))

    def error(self, test_num, label, info=None):
        """ format a test record with status 'error' """
        test = self.test('error', label)
        self.stream.writeln(self.serialize(test))

    def skip(self, test_num, label, info=None):
        """ format a test record with status 'omit' """
        test = self.test('omit', label)
        self.stream.writeln(self.serialize(test))

    def todo(self, test_num, label, info=None):
        """ format a test record with status 'todo' """
        test = self.test('todo', label)
        self.stream.writeln(self.serialize(test))

    def note(self, text):
        """ format a note record """
        self.stream.writeln(self.serialize({'type': 'note', 'text': text}))

    def final(self, counts, tally=False):
        """ format a final or tally record """
        final = {
            'type': 'final',
            'time': self.elapsed_time(),
            'counts': counts,
        }
        if tally:
            final['type'] = 'tally'
        self.stream.writeln(self.serialize(final, final=True))


class TAPJFormatter(SerializingTAPFormatter):
    """ Format test results in the TAP-J format """

    def __init__(self, stream):
        super(TAPJFormatter, self).__init__(stream)

    def serialize(self, data, final=False):
        return json.dumps(data)
        # more compact
        # return json.dumps(data, separators=(',',':'))


class TAPYFormatter(SerializingTAPFormatter):
    """ Format test results in the TAP-Y format """

    def __init__(self, stream):
        super(TAPYFormatter, self).__init__(stream)

    def serialize(self, data, final=False):
        explicit_end = final
        return yaml.safe_dump(data,
                              default_flow_style=False,
                              explicit_start=True,
                              explicit_end=explicit_end)
