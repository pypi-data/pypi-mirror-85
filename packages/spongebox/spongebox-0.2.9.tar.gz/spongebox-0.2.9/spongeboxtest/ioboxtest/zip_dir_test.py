import unittest
from spongebox.iobox import zip_dir,list_all_files
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # zip_dir("E:\\download\\haha.zip", "E:\\download\\test")
        self.assertEqual(True, True)

    def test_something1(self):
        print(os.getcwd())
        print(list_all_files("testzip"))
        zip_dir("E:\\download\\momo.zip", "testzip")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
