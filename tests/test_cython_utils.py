import unittest

from picobuild import get_cython_build_dir


class TestCythonUtils(unittest.TestCase):
    def test_get_cython_build_dir(self):
        result = get_cython_build_dir()
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("build/cython."))
