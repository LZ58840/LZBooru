import requests
from datetime import datetime, timedelta, date
import calendar
from dotenv import dotenv_values


config = dotenv_values(".env")
BOORU_URL = config["URL"]
PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search"
HEADERS = { "x-api-key": config["API_KEY"] }


def get_subreddits():
    subreddits_json = requests.get(url=f"{BOORU_URL}/subreddit", headers=HEADERS).json()
    return subreddits_json


def get_subreddit_submissions_json(subreddit_json):
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

    submissions_json = requests.get(url=f"{PUSHSHIFT_URL}/submission", params=PARAMS).json()
    return submissions_json["data"]


def update_subreddits(subreddits_json):
    for subreddit_json in subreddits_json:
        updated_utc = subreddit_json["updated"] if subreddit_json["updated"] is not None else subreddit_json["created"]
        subreddit_json["updated"] = calendar.timegm((date.fromtimestamp(updated_utc) + timedelta(days=1)).timetuple())
    PARAMS = subreddits_json
    return requests.patch(url=f"{BOORU_URL}/subreddit", params=PARAMS, headers=HEADERS)


def post_submissions(formatted_submissions_json):
    PARAMS = formatted_submissions_json
    return requests.post(url=f"{BOORU_URL}/submissions", params=PARAMS, headers=HEADERS)


def format_submission_json(submission_json):
    return {
        "url": submission_json["id"],
        "title": submission_json["title"],
        "contributor": submission_json["author"],
        "subreddit": submission_json["subreddit"],
        "created": submission_json["created_utc"],
        "flair": submission_json["link_flair_text"] if "link_flair_text" in submission_json else None,
        "image": submission_json["url"],
        "nsfw": submission_json["over_18"]
    }
