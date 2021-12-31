import requests
from dotenv import dotenv_values
from api import pmaw_api


config = dotenv_values(".env")
BOORU_URL = config["URL"]
BOORU_HEADERS = { "x-api-key": config["API_KEY"] }


def get_subreddits():
    subreddits_json = requests.get(url=f"{BOORU_URL}/subreddit", headers=BOORU_HEADERS).json()
    return subreddits_json


def get_subreddit_submissions_json(subreddit_json):
    after_utc = subreddit_json["updated"] if subreddit_json["updated"] is not None else subreddit_json["created"]
    submissions_query = pmaw_api.search_submissions(after=after_utc, subreddit=subreddit_json["name"], limit=None)
    submissions_json = list(submissions_query)
    return submissions_json


def post_links(formatted_links_json):
    payload = formatted_links_json
    return requests.post(url=f"{BOORU_URL}/link", json=payload, headers=BOORU_HEADERS)


def post_submissions(formatted_submissions_json):
    payload = formatted_submissions_json
    return requests.post(url=f"{BOORU_URL}/submission", json=payload, headers=BOORU_HEADERS)
