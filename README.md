Catapult
========

Catapult provides [TAP](http://testanything.org/) output for Python unittest test suites.

Currently it supports the [TAP][] (12), [TAP-Y][], and [TAP-J][] formats. See
[catapult/tests/run.py][] for an example of how to use catapult in your test runner.

[TAP]: http://testanything.org/tap-specification.html
[TAP-Y]: https://github.com/rubyworks/tapout/wiki/TAP-Y-J-Specification
[TAP-J]: https://github.com/rubyworks/tapout/wiki/TAP-Y-J-Specification
[catapult/tests/run.py]: https://github.com/jcelliott/catapult/blob/master/catapult/tests/run.py

Nose plugin
-----------

Catapult also provides a plugin for [nose][]. After installing, use it like this:

    nosetests --with-catapult --catapult-format=tap-j

where the format can be one of `tap`, `tap-j` (default), or `tap-y`

[nose]: https://nose.readthedocs.org/en/latest/

Installing
----------

Install from PyPI with pip:

    pip install catapult

