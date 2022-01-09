from parsa.patterns import GENERIC_PATTERN, IMGUR_PATTERN, REDDIT_PATTERN
import re
import html


def format_submission_json(submission_json):
    """
    Formats submission info as Submission.

    :param submission_json: JSON formatted dict of submission from reddit
    :return: JSON formatted dict of a Submission entry
    """

    return {
        "id": submission_json["id"],
        "title": html.unescape(submission_json["title"])[:300],
        "author": submission_json["author"],
        "subreddit": submission_json["subreddit"],
        "created": submission_json["created_utc"],
        "flair": submission_json["link_flair_text"] if "link_flair_text" in submission_json else None,
        "nsfw": submission_json["over_18"]
        }


def format_link_json(submission_json):
    """
    Formats submission info as Link.

    :param submission_json: JSON formatted dict of submission from reddit
    :return: JSON formatted dict of a Link entry
    """

    return {
        "url": submission_json["url"], 
        "created": submission_json["created_utc"],
        "id": submission_json["id"],
        "type": _get_link_type(submission_json["url"])
        }


def _get_link_type(link):
    """
    Classifies link based on URL patterns.

    :param link: URL formatted str
    :return: link type
    """
    if re.match(IMGUR_PATTERN, link) is not None:
        return "imgur"
    elif re.match(REDDIT_PATTERN, link) is not None:
        return "reddit"
    elif re.match(GENERIC_PATTERN, link) is not None:
        return "generic"
    else:
        return None
