from prawcore import NotFound
from api import praw_api


def subreddit_exists(subreddit_name):
    """
    Checks if a subreddit exists given a name.

    :param subreddit_name: a possible name of a subreddit
    :return: True if subreddit exists, False otherwise
    """

    try:
        praw_api.subreddits.search_by_name(subreddit_name, exact=True)

    except NotFound:
        return False

    return True


def get_subreddit_created(subreddit_name):
    """
    Gets the subreddit created timestamp.

    :param subreddit_name: a name of a valid subreddit
    :return: the created timestamp of the subreddit in seconds
    """

    subreddit = praw_api.subreddit(subreddit_name)

    return int(subreddit.created_utc)
