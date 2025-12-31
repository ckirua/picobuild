import unittest

import picobuild


class TestPicobuild(unittest.TestCase):
    def test_all_exports(self):
        for name in picobuild.__all__:
            self.assertTrue(hasattr(picobuild, name))
