from time import sleep
import praw
from praw.exceptions import RedditAPIException


LOGIN_TRIES = 5
LOGIN_SLEEP = 5


def login_ro(client_id, client_secret, user_agent):
    for attempt in range(LOGIN_TRIES):
        try:
            instance = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
            )
            return instance
        except (RedditAPIException, Exception):
            sleep(LOGIN_SLEEP)
    return None
