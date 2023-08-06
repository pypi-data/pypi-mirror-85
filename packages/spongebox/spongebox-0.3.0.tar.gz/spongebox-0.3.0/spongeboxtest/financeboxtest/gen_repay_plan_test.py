import unittest
from spongebox.financebox.loanbox import repay_plan_factory


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.prin = 10000
        self.mon_rate = 0.01
        self.n_periods = 3

    def test_something0(self):
        _ = (repay_plan_factory("等额本息"))(self.prin,self.mon_rate,self.n_periods)
        print(_)
        # self.assertEqual(True, False)
        # self.assertListEqual()

    def test_something1(self):
        _ = (repay_plan_factory("等额本金"))(self.prin, self.mon_rate, self.n_periods)
        print(_)
        # self.assertListEqual()

    def test_something2(self):
        _ = (repay_plan_factory("等本等息"))(self.prin, self.mon_rate, self.n_periods)
        print(_)
        # self.assertListEqual()

if __name__ == '__main__':
    unittest.main()
