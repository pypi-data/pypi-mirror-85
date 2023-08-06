import unittest
from spongebox.timebox import *

class MyTestCase(unittest.TestCase):
    def test_case1(self):
        self.assertEqual(format_match(20200302), "%Y%m%d")

    def test_case2(self):
        self.assertEqual(format_match("20200302"), "%Y%m%d")

    def test_case3(self):
        self.assertEqual(format_match("2020-03-02"), "%Y-%m-%d")

    def test_case4(self):
        self.assertEqual(format_match("2020-03-02 15:20:02"), "%Y-%m-%d %H:%M:%S")

    def test_case5(self):
        self.assertRaises(UnknownDateFormatError, format_match, "202502-36 15:20:02")

    def test_case6(self):
        self.assertEqual(format_match("202009121546"), "%Y%m%d%H%M")

    def test_case7(self):
        self.assertEqual(format_match("20200912154634"), "%Y%m%d%H%M%S")

if __name__ == '__main__':
    unittest.main()
