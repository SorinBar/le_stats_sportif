import requests
import json
import unittest


class TestWebserver(unittest.TestCase):
    def setUp(self):
        pass

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        print()
    