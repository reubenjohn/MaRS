import sys
from unittest import TestCase

from mars.main import hello


class Test(TestCase):
    def test_python_version(self):
        python_version = sys.version
        splits = python_version.split(".")
        self.assertEqual("3", splits[0])
        self.assertGreaterEqual(int(splits[1]), 7)

    def test_hello(self):
        self.assertEqual(hello(), 1)
