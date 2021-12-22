import requests
from datetime import datetime, timedelta
from dotenv import dotenv_values
from multiprocessing import cpu_count, Pool

config = dotenv_values(".env")
BOORU_URL = config["URL"]
PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search"
HEADERS = { "x-api-key": config["API_KEY"] }


def get_subreddits():
    subreddits = requests.get(url=f"{BOORU_URL}/subreddit", headers=HEADERS)
    subreddits_json = subreddits.json()
    return subreddits_json


def get_subreddit_submissions(subreddit_json):
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


def update_booru_subreddit(booru_subreddit_json):
    return requests.patch(url=f"{BOORU_URL}/subreddit/{booru_subreddit_json['name']}")


def _parse_pushshift_submission(pushshift_submission_json):
    return {
        "url": pushshift_submission_json["id"],
        "title": pushshift_submission_json["title"],
        "contributor": pushshift_submission_json["author"],
        "subreddit": pushshift_submission_json["subreddit"],
        "created": pushshift_submission_json["created_utc"],
        "flair": pushshift_submission_json["link_flair_text"],
        "image": pushshift_submission_json["url"],
        "nsfw": pushshift_submission_json["over_18"]
    }
