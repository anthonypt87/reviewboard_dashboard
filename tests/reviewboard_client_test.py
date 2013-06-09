import unittest

import mock
from reviewboard_client import ReviewboardClient
from reviewboard_client import ReviewRequest


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
				'status': 'pending', 'id': 3
			}
		)


class ReviewboardClientTest(unittest.TestCase):

	def test_get_review_requests(self):
		reviewboard_client = ReviewboardClient(MockRBClient())
		reviews = list(reviewboard_client.get_review_requests())
		self.assertEqual(len(reviews), 2)


class ReviewRequestTest(unittest.TestCase):

	def test_create_from_rb_client_review_request(self):
		rb_client_review_request = mock.Mock(
			get_submitter=lambda: mock.Mock(
				fields={
					'username': 'anthony'
				}
			),
			fields={
				u'branch': u'anthony/anthony_is_the_best',
				u'bugs_closed': [u'47909'],
				u'changenum': None,
				u'description': u'Primary reviewer: andy\nAnthony is the best',
				u'id': 32868,
				u'last_updated': u'2013-06-09 14:10:46',
				u'public': True,
				u'status': u'pending',
				u'summary': u'Proving once and for all he is the greatest',
				u'target_groups': [
					{
						u'href': u'https://reviewboard.anthony.com/api/groups/group1/',
						u'method': u'GET',
						u'title': u'group1'
					}
				],
				u'target_people': [
					{
						u'href': u'https://reviewboard.anthony.com/api/users/andy/',
						u'method': u'GET',
						u'title': u'andy'
					}
				],
				u'testing_done': u'Wrote some tests',
				u'time_added': u'2013-06-06 09:50:57'
			},
			get_reviews=lambda: [
				mock.Mock(
					fields={
						u'ship_it': True,
					},
					get_user=lambda: mock.Mock(
						fields={
							'username': 'andy'
						}
					)
				)
			]
		)
		review_request = ReviewRequest.create_from_rb_client_review_request(rb_client_review_request)
		self.assertEqual(review_request.id, 32868)
		self.assertEqual(review_request.submitter, 'anthony')
		self.assertEqual(review_request.reviewers, ['andy'])
		self.assertEqual(review_request.summary, rb_client_review_request.fields['summary'])
		self.assertEqual(review_request.description, rb_client_review_request.fields['description'])
		self.assertEqual(
			review_request.reviews,
			[{
				'ship_it': True,
				'reviewer': 'andy'
			}]
		)
