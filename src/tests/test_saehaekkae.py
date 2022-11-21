import unittest
from saehaekkae import main

class TestSaehaekkae(unittest.TestCase):

    def test_main(self):
        self.assertEqual(0, main())
