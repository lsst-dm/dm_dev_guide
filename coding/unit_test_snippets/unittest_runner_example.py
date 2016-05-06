import unittest

import lsst.utils.tests as utilsTests


class DemoTestCase(utilsTests.TestCase):
    """Demo test case."""

    def testDemo(self):
        assert True


def suite():
    """Returns a suite containing all the test cases in this module."""
    utilsTests.init()

    suites = []
    # Test suites for this module here
    suites += unittest.makeSuite(DemoTestCase)
    # MemoryTestCase to find C++ memory leaks
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)


def run(exit=False):
    """Run the tests"""
    utilsTests.run(suite(), exit)


if __name__ == "__main__":
    run(True)
