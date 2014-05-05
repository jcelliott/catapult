from unittest import TestCase, skip
import time
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class ExampleTest(TestCase):

    def test_something(self):
        """ A test to check something """
        time.sleep(0.5)
        self.assertEqual("something", "something")

    def test_something_else(self):
        time.sleep(0.5)
        print("This is some text that shouldn't interfere with the TAP output")
        self.assertEqual("something", "else")

    def test_number_one(self):
        """ Test the number of things is equal to one """
        time.sleep(0.5)
        log.info("This is a log message that shouldn't interfere with the TAP output")
        self.assertTrue(1 == 1)

    @skip("this test is pointless")
    def test_skipping(self):
        """ This is something that should be skipped """
        self.assertTrue("the world is flat")

    def test_example_1(self):
        """ An example test """
        time.sleep(0.5)
        print("This is some more text that shouldn't interfere with the TAP output")
        self.assertTrue(True)

    def test_example_2(self):
        """ Another example test """
        time.sleep(0.5)
        log.error("This is another log message that shouldn't interfere with the TAP output")
        raise Exception("this test will error")
        self.assertTrue(True)
