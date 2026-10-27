import asyncio
import math
import unittest

from core.orchestrator import Orchestrator
from core.sample_data import load_activities, load_transactions


class DemoTests(unittest.TestCase):
    def test_sample_rows_are_recent_and_keep_real_csv_values(self):
        transactions = load_transactions(now='2026-10-27')
        activities = load_activities(now='2026-10-27')
        self.assertGreater(len(transactions), 0)
        self.assertGreater(len(activities), 0)
        self.assertEqual(transactions['timestamp'].max().date().isoformat(), '2026-10-27')
        self.assertEqual(activities['timestamp'].max().date().isoformat(), '2026-10-27')
        self.assertIn('Whole Foods Market', set(transactions['merchant']))

    def test_one_shot_summary_includes_all_three_domains(self):
        result = asyncio.run(Orchestrator().run_once())
        self.assertEqual(result['data_freshness'], {'activity': True, 'finance': True, 'email': True})
        finance = result['detailed_insights']['finance']['insights']
        self.assertGreater(finance['transaction_count'], 0)
        self.assertGreater(finance['total_spent'], 0)
        self.assertTrue(math.isfinite(finance['average_transaction']))


if __name__ == '__main__':
    unittest.main()
