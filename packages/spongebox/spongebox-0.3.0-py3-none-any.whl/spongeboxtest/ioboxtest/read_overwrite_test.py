import unittest
from spongebox.iobox import read_overwrite
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(os.getcwd())
        read_overwrite("test.txt",lambda x:"haha")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
