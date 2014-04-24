from unittest import TestCase
import time


class MoreTest(TestCase):

    def test_more_things(self):
        """ A test for more things """
        time.sleep(0.5)
        self.assertNotEqual("More", "Things")

    def test_foo_bar(self):
        """ A test to verify that the foo succesfully bars """
        time.sleep(0.5)
        self.assertTrue("foo" != "bar")
