import unittest

from picobuild import Extension, find_packages, setup


class TestSetuptools(unittest.TestCase):
    def test_imports(self):
        self.assertIsNotNone(Extension)
        self.assertIsNotNone(find_packages)
        self.assertIsNotNone(setup)
