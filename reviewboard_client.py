"""Thin wrapper around ``rbtools.api.client.RBClient```"""

class ReviewboardClient(object):
	def __init__(self, rb_client):
		self._rb_client = rb_client
		self._root = self._rb_client.get_root()

	def get_review_requests(self, **filters):
		review_request_list_resource = self._root.get_review_requests(**filters)
		while True:
			for review_request in review_request_list_resource:
				yield review_request
			review_request_list_resource = review_request_list_resource.get_next(**filters)



