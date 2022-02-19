# -*- coding: utf-8 -*-
import unittest
from nagiosplugin.state import Ok, Warning, Unknown, Critical, worst


class StateTest(unittest.TestCase):

    def test_str(self):
        self.assertEqual('ok', str(Ok))

    def test_int(self):
        self.assertEqual(3, int(Unknown))

    def test_cmp_less(self):
        self.assertTrue(Warning < Critical)

    def test_cmp_greater(self):
        self.assertTrue(Warning > Ok)

    def test_worst(self):
        self.assertEqual(Critical, worst([Ok, Critical, Warning]))

    def test_worst_of_emptyset_is_ok(self):
        self.assertEqual(Ok, worst([]))
