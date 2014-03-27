from unittest import TestCase


class DemonstrationTest(TestCase):

    def test_a_piece_of_code(self):
        """ Test that the code checks out """
        self.assertEqual("piece of code", "piece of code")

    def test_another_piece_of_code(self):
        """ Test that the another equals another """
        self.assertEqual("another", "another")

    def test_a_number(self):
        """ Test all the numbers """
        self.assertTrue(3 == 2)
