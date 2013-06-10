import argparse
from flask import Flask

from collect_reviewboard_stats import collect_reviewboard_stats


app = Flask(__name__)


@app.route('/')
def reviewboard_dashboard():
	reviewboard_stats = collect_reviewboard_stats(
		app.config['reviewboard_url'],
		app.config['reviewboard_users']
	)
	return str(reviewboard_stats)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Start up server to display reviewboard stats')
	parser.add_argument('reviewboard_url', help='Url to the root of the reviewboard server')
	parser.add_argument('--reviewboard-users', dest='reviewboard_users', help='URL of reviewboard users to make server for', nargs='*')
	args = parser.parse_args()

	app.config['reviewboard_url'] = args.reviewboard_url
	app.config['reviewboard_users'] = args.reviewboard_users

	app.run()
