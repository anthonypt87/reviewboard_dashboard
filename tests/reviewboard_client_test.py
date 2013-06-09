import unittest

import mock
from reviewboard_client import ReviewboardClient

class MockRBClient(object):

	def get_root(self):
		return mock.Mock(
			get_review_requests=mock.MagicMock(
				return_value=self._create_chained_review_requests_list_resource()
			)
		)

	def _create_chained_review_requests_list_resource(self):
		last_review_reqests_list_resource = self._create_review_requests_list_resource()
		return self._create_review_requests_list_resource(
			next_resource=last_review_reqests_list_resource
		)

	def _create_review_requests_list_resource(self, next_resource=None):
		review_requests_list_resource = mock.Mock(
			__iter__=mock.Mock(return_value=iter([self._create_mock_review_resource()]))
		)
		if next_resource is None:
			review_requests_list_resource.get_next.side_effect = StopIteration
		else:
			review_requests_list_resource.get_next.return_value = next_resource

		return review_requests_list_resource

	def _create_mock_review_resource(self):
		return mock.Mock(
			fields={
				'status': 'pending',
				'id': 3
			}
		)


class ReviewboardClientTest(unittest.TestCase):

	def setUp(self):
		self._mock_rb_client_patcher = mock.patch('reviewboard_client.RBClient', MockRBClient)
		self._mock_rb_client = self._mock_rb_client_patcher.start()()

	def tearDown(self):
		self._mock_rb_client_patcher.stop()

	def test_get_review_request(self):
		reviewboard_client = ReviewboardClient(self._mock_rb_client)
		reviews = list(reviewboard_client.get_review_requests())
		self.assertEqual(len(reviews), 2)
