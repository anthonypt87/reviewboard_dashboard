import os
import pickle
import string
import unicodedata

from reviewboard_client import ReviewboardClient


def collect_reviewboard_stats(reviewboard_url, usernames, client_kwargs=None, **get_review_requests_kwargs):
	if client_kwargs is None:
		client_kwargs = {}
	reviewboard_client = ReviewboardClient.create_using_reviewboard_url(reviewboard_url, **client_kwargs)
	return dict(
		(
			username,
			list(
				reviewboard_client.get_review_requests(to_users_directly=username, **get_review_requests_kwargs)
			)
		) for username in usernames
	)


def cached_collect_reviewboard_stats(reviewboard_url, usernames, cache_directory, **get_review_requests_kwargs):
	filename = u'%s+%s.pickle' % (reviewboard_url, '_'.join(sorted(usernames)))
	filename = _remove_disallowed_filename_characters(filename)
	full_path = os.path.join(cache_directory, filename)

	if os.path.exists(full_path):
		with open(full_path) as pickle_file:
			return pickle.loads(pickle_file.read())

	else:
		stats = collect_reviewboard_stats(reviewboard_url, usernames, **get_review_requests_kwargs)
		if not os.path.exists(cache_directory):
			os.makedirs(cache_directory)
		with open(full_path, 'w') as pickle_file:
			pickle_file.write(pickle.dumps(stats))


def _remove_disallowed_filename_characters(filename):
	"""Removes invalid characters from the filename."""
	valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
	return ''.join(c for c in cleaned_filename if c in valid_filename_chars)
