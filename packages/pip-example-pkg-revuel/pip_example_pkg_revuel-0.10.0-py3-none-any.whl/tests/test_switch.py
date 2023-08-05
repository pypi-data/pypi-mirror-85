""" Just a test file """
import unittest
from example_pkg.switch import switch, _say_hello, _say_goodbye, _unknown_salute

class TestSwitch(unittest.TestCase):
    def test_say_hello(self):
        self.assertEqual(_say_hello(), switch(0))

    def test_say_goodbye(self):
        self.assertEqual(_say_goodbye(), switch(1))

    def test_unknown_salute(self):
        self.assertEqual(_unknown_salute(), switch(2))

if __name__ == '__main__':
    unittest.main()
