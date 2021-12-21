import requests
from datetime import datetime, timedelta
from dotenv import dotenv_values
from multiprocessing import cpu_count, Pool

config = dotenv_values(".env")
BOORU_URL = config["URL"]
PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search"
HEADERS = { "x-api-key": config["API_KEY"] }


def get_booru_subreddits():
    subreddits = requests.get(url=f"{BOORU_URL}/subreddit", headers=HEADERS)
    subreddits_json = subreddits.json()
    return subreddits_json
    
    for subreddit in subreddits_json:
        after_utc = subreddit["updated"] if subreddit["updated"] is not None else subreddit["created"]
        after_datetime = datetime.utcfromtimestamp(after_utc)
        after = after_datetime.strftime('%Y-%m-%d')
        before = (after_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
        PARAMS = {
            "subreddit": subreddit["name"],
            "after": after,
            "before": before,
            "size": 500
        }

        submissions = requests.get(url=f"{PUSHSHIFT_URL}/submission", params=PARAMS)
        submissions_json = submissions.json()
        for submission in submissions_json["data"]:
            pass
            # parse submission
        # post submission
        # update subreddit updated time


def get_pushshift_submissions(subreddit_json):
    after_utc = subreddit_json["updated"] if subreddit_json["updated"] is not None else subreddit_json["created"]
    after_datetime = datetime.utcfromtimestamp(after_utc)
    after = after_datetime.strftime('%Y-%m-%d')
    before = (after_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
    PARAMS = {
        "subreddit": subreddit_json["name"],
        "after": after,
        "before": before,
        "size": 500
    }

    submissions = requests.get(url=f"{PUSHSHIFT_URL}/submission", params=PARAMS)
    submissions_json = submissions.json()
    return submissions_json


def update_booru_subreddit(subreddit_json):
    pass
    # process some stuff here


def _parse_pushshift_submission(submission_json):
    pass
