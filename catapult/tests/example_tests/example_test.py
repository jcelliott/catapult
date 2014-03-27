from unittest import TestCase, skip


class ExampleTest(TestCase):

    def test_something(self):
        """ A test to check something """
        self.assertEqual("something", "something")

    def test_something_else(self):
        self.assertEqual("something", "else")

    def test_number_one(self):
        """ Test the number of things is equal to one """
        self.assertTrue(1 == 1)

    @skip("this test is pointless")
    def test_skipping(self):
        """ This is something that should be skipped """
        self.assertTrue("the world is flat")
