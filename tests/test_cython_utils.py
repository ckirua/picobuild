import unittest

from picobuild import get_cython_build_dir, Extension, cythonize


class TestCythonUtils(unittest.TestCase):
    def test_get_cython_build_dir(self):
        result = get_cython_build_dir()
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("build/cython."))

    def test_cythonize(self):
        result = cythonize([Extension("test", ["test.pyx"])])
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], Extension)
        self.assertEqual(result[0].name, "test")
        self.assertEqual(result[0].sources, ["test.pyx"])
