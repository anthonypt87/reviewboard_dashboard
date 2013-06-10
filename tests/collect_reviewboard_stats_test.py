import unittest

import mock

from reviewboard_client import ReviewRequest
from collect_reviewboard_stats import collect_reviewboard_stats


class CollectReviewboardStatsTest(unittest.TestCase):

	def test_collect_reviewboard_stats(self):
		request_submitted_from_anthony = self._create_mock_request('anthony', 'andy')
		request_submitted_from_andy = self._create_mock_request('andy', 'anthony')
		with mock.patch(
			'collect_reviewboard_stats.ReviewboardClient'
		) as mock_reviewboard_client_class:
			mock_reviewboard_client = mock_reviewboard_client_class.return_value
			mock_reviewboard_client.get_review_requests.side_effect = [
				[request_submitted_from_anthony],
				[request_submitted_from_andy],
			]
			reviewboard_url = 'http://reviewboard.anthony.com'
			collected_stats = collect_reviewboard_stats(reviewboard_url, ['anthony', 'andy'])

		self.assertEqual(
			collected_stats,
			{
				'anthony': [request_submitted_from_anthony],
				'andy': [request_submitted_from_andy]
			}
		)

	def _create_mock_request(self, submitter, reviewer):
		return ReviewRequest(
			1,
			submitter,
			[reviewer],
			'Summary',
			'Description',
			[{
				'ship_it': True,
				'reviewer': reviewer
			}]
		)
