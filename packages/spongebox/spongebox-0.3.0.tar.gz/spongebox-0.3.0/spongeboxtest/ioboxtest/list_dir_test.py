import unittest
from spongebox.iobox import list_dir

class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(list(list_dir(".")))
        self.assertEqual(True, True)

    def test_something1(self):
        print(list(list_dir(".",judge_func=lambda x:"test" in x)))
        self.assertEqual(True, True)

    def test_something2(self):
        print(list(list_dir(".",exp="\.py")))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
