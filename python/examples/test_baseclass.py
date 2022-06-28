import unittest


class BaseClass:
    def testParam(self):
        self.assertLess(self.PARAM, 5)


class ThisIsTest1(BaseClass, unittest.TestCase):
    PARAM = 3


if __name__ == "__main__":
    unittest.main()
