# -*- coding: utf-8 -*-
from nagiosplugin.result import Result, Results
from nagiosplugin.state import Ok, Warning, Critical, Unknown
import nagiosplugin

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class ResultTest(unittest.TestCase):

    def test_resorce_should_be_none_for_resourceless_metric(self):
        self.assertIsNone(Result(Ok).resource)

    def test_metric_resorce(self):
        res = object()
        m = nagiosplugin.Metric('foo', 1, resource=res)
        self.assertEqual(Result(Ok, metric=m).resource, res)

    def test_context_should_be_none_for_contextless_metric(self):
        self.assertIsNone(Result(Ok).context)

    def test_metric_context(self):
        ctx = object()
        m = nagiosplugin.Metric('foo', 1, contextobj=ctx)
        self.assertEqual(Result(Ok, metric=m).context, ctx)

    def test_str_metric_with_hint(self):
        self.assertEqual('2 (unexpected)',
                         str(Result(Warning, 'unexpected',
                                    nagiosplugin.Metric('foo', 2))))

    def test_str_metric_only(self):
        self.assertEqual(
            '3', str(Result(Warning, metric=nagiosplugin.Metric('foo', 3))))

    def test_str_hint_only(self):
        self.assertEqual('how come?', str(Result(Warning, 'how come?')))

    def test_str_empty(self):
        self.assertEqual('', str(Result(Warning)))


class ResultsTest(unittest.TestCase):

    def test_lookup_by_metric_name(self):
        r = Results()
        result = Result(Ok, '', nagiosplugin.Metric('met1', 0))
        r.add(result, Result(Ok, 'other'))
        self.assertEqual(r['met1'], result)

    def test_lookup_by_index(self):
        r = Results()
        result = Result(Ok, '', nagiosplugin.Metric('met1', 0))
        r.add(Result(Ok, 'other'), result)
        self.assertEqual(r[1], result)

    def test_len(self):
        r = Results()
        r.add(Result(Ok), Result(Ok), Result(Ok))
        self.assertEqual(3, len(r))

    def test_iterate_in_order_of_descending_states(self):
        r = Results()
        r.add(Result(Warning), Result(Ok), Result(Critical), Result(Warning))
        self.assertEqual([Critical, Warning, Warning, Ok],
                         [result.state for result in r])

    def test_most_significant_state_shoud_raise_valueerror_if_empty(self):
        with self.assertRaises(ValueError):
            Results().most_significant_state

    def test_most_significant_state(self):
        r = Results()
        r.add(Result(Ok))
        self.assertEqual(Ok, r.most_significant_state)
        r.add(Result(Critical))
        self.assertEqual(Critical, r.most_significant_state)
        r.add(Result(Warning))
        self.assertEqual(Critical, r.most_significant_state)

    def test_most_significant_should_return_empty_set_if_empty(self):
        self.assertEqual([], Results().most_significant)

    def test_most_signigicant(self):
        r = Results()
        r.add(Result(Ok), Result(Warning), Result(Ok), Result(Warning))
        self.assertEqual([Warning, Warning],
                         [result.state for result in r.most_significant])

    def test_first_significant(self):
        r = Results()
        r.add(Result(Critical), Result(Unknown, 'r1'), Result(Unknown, 'r2'),
              Result(Ok))
        self.assertEqual(Result(Unknown, 'r1'), r.first_significant)

    def test_contains(self):
        results = Results()
        r1 = Result(Unknown, 'r1', nagiosplugin.Metric('m1', 1))
        results.add(r1)
        self.assertTrue('m1' in results)
        self.assertFalse('m2' in results)

    def test_add_in_init(self):
        results = Results(Result(Unknown, 'r1'), Result(Unknown, 'r2'))
        self.assertEqual(2, len(results))

    def test_add_should_fail_unless_result_passed(self):
        with self.assertRaises(ValueError):
            Results(True)
