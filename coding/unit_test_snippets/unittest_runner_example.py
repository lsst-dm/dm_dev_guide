import unittest
import lsst.utils.tests


def setup_module(module):
    lsst.utils.tests.init()


class DemoTestCase(lsst.utils.tests.TestCase):
    """Demo test case."""

    def testDemo(self):
        self.assertNotIn("i", "team")


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
