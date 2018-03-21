import unittest
import math


class DemoTestCase1(unittest.TestCase):
    """Demo test case 1."""

    def testDemo(self):
        self.assertGreater(10, 5)
        with self.assertRaises(TypeError):
            1 + "2"


class DemoTestCase2(unittest.TestCase):
    """Demo test case 2."""

    def testDemo1(self):
        self.assertNotEqual("string1", "string2")

    def testDemo2(self):
        self.assertAlmostEqual(3.14, math.pi, places=2)


if __name__ == "__main__":
    unittest.main()
