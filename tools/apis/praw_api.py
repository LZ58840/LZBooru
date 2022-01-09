from praw import Reddit
from praw.exceptions import RedditAPIException
from time import sleep
from dotenv import dotenv_values


config = dotenv_values(".env")


LOGIN_TRIES = 5
LOGIN_SLEEP = 5


CLIENT_ID = config["REDDIT_CLIENT_ID"]
CLIENT_SECRET = config["REDDIT_CLIENT_SECRET"]
USER_AGENT = config["REDDIT_USER_AGENT"]


def login_ro():
    """Creates a Read-only Reddit instance."""
    for _ in range(LOGIN_TRIES):
        try:
            instance = Reddit(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                user_agent=USER_AGENT,
            )
            return instance
        except (RedditAPIException, Exception):
            sleep(LOGIN_SLEEP)
    return None
