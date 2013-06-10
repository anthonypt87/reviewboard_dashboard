import os
import tempfile
import unittest

import mock

import collect_reviewboard_stats
from reviewboard_client import ReviewRequest


def create_mock_request(submitter, reviewer):
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


class CollectReviewboardStatsTest(unittest.TestCase):

	def test_collect_reviewboard_stats(self):
		request_submitted_from_anthony = create_mock_request('anthony', 'andy')
		request_submitted_from_andy = create_mock_request('andy', 'anthony')
		with mock.patch(
			'collect_reviewboard_stats.ReviewboardClient.create_using_reviewboard_url'
		) as mock_reviewboard_client_class:
			mock_reviewboard_client = mock_reviewboard_client_class.return_value
			mock_reviewboard_client.get_review_requests.side_effect = [
				[request_submitted_from_anthony],
				[request_submitted_from_andy],
			]
			reviewboard_url = 'http://reviewboard.anthony.com'
			collected_stats = collect_reviewboard_stats.collect_reviewboard_stats(reviewboard_url, ['anthony', 'andy'])

		self.assertEqual(
			collected_stats,
			{
				'anthony': [request_submitted_from_anthony],
				'andy': [request_submitted_from_andy]
			}
		)


class CachedCollectReviewboardStatsTest(unittest.TestCase):

	def test_cached_collect_reviewboard_stats(self):
		tempdir = tempfile.gettempdir()

		request = create_mock_request('anthony', 'andy')
		with mock.patch(
			'collect_reviewboard_stats.collect_reviewboard_stats',
			return_value=request
		) as mock_collect_reviewboard_stats:
			result_1 = collect_reviewboard_stats.cached_collect_reviewboard_stats('http://reviewboard.anthony.com', ['anthony'], tempdir)
			result_2 = collect_reviewboard_stats.cached_collect_reviewboard_stats('http://reviewboard.anthony.com', ['anthony'], tempdir)
			self.assertEqual(result_1.id, result_2.id)
			self.assertTrue(mock_collect_reviewboard_stats.call_count < 2)
