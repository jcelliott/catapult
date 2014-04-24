from unittest import TestCase
import time


class DemonstrationTest(TestCase):

    result = None  # used to return arbitrary data to the test runner

    def test_a_piece_of_code(self):
        """ Test that the code checks out """
        time.sleep(0.5)
        self.assertEqual("piece of code", "piece of code")

    def test_another_piece_of_code(self):
        """ Test that the another equals another """
        time.sleep(0.5)
        self.assertEqual("another", "another")
        self.result = {'testing': 'here are some results', 'data': 23423}

    def test_a_number(self):
        """ Test all the numbers """
        time.sleep(0.5)
        self.assertTrue(3 == 2)

    def test_bad_foobar(self):
        """ Test that a bad foobar will fail validation """
        time.sleep(0.5)
        self.assertFalse(False)
