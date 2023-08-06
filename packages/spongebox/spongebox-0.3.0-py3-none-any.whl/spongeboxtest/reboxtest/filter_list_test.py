import unittest
from spongebox.rebox import filter_list


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertListEqual(list(filter_list(list("abc"), judge_func=lambda x: x == "a")), ["a"])

    def test_something1(self):
        self.assertListEqual(list(filter_list(list("abc"), pattern="a")), ["a"])


if __name__ == '__main__':
    unittest.main()
