import os
import tempfile
import unittest

from picobuild import get_cython_build_dir, Extension, cythonize


class TestCythonUtils(unittest.TestCase):
    def test_get_cython_build_dir(self):
        result = get_cython_build_dir()
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("build/cython."))

    def test_cythonize(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_pyx = os.path.join(tmpdir, "test.pyx")
            with open(test_pyx, "w") as f:
                f.write("def hello(): pass\n")
            result = cythonize([Extension("test", [test_pyx])])
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], Extension)
            self.assertEqual(result[0].name, "test")
