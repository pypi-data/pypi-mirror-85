import unittest
from spongebox.structbox import flatten_list

class MyTestCase(unittest.TestCase):
    def test_something0(self):
        self.assertListEqual(flatten_list([1,[2,3,[4,5],6],7]), [i for i in range(1,8)])


if __name__ == '__main__':
    unittest.main()
