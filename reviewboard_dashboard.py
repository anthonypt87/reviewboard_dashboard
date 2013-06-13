import datetime

import argparse
from flask import Flask
from flask import render_template

import collect_reviewboard_stats


app = Flask(__name__)


@app.route('/')
def reviewboard_dashboard():
	client_kwargs = {
		'username': app.config['username'],
		'password': app.config['password']
	}
	reviewboard_stats = collect_reviewboard_stats.cached_collect_reviewboard_stats(
		app.config['reviewboard_url'],
		app.config['reviewboard_users'],
		client_kwargs=client_kwargs,
		max_results=200,
		last_updated_from=datetime.datetime.now() - datetime.timedelta(days=14),
		status='pending',
		cache_directory=app.config['cache_directory'],
	)
	return render_template(
		'reviewboard_dashboard.html',
		reviewboard_stats=reviewboard_stats,
		review_url_generator=lambda review_id: '%s/r/%s' % (app.config['reviewboard_url'], review_id)
	)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Start up server to display reviewboard stats')
	parser.add_argument('reviewboard_url', help='Url to the root of the reviewboard server')
	parser.add_argument('--reviewboard-users', help='URL of reviewboard users to make server for', nargs='*')
	parser.add_argument('--username', help='Reviewboard username')
	parser.add_argument('--password', help='Reviewboard password')
	parser.add_argument('--cache-directory', help='Cache directory (janky way to cache reviewboard results)')
	args = parser.parse_args()

	app.config['reviewboard_url'] = args.reviewboard_url
	app.config['reviewboard_users'] = args.reviewboard_users
	app.config['username'] = args.username
	app.config['password'] = args.password
	app.config['cache_directory'] = args.cache_directory

	app.run()
