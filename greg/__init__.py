import logging
from greg.api import get_subreddits, post_submissions, post_links
from greg.proc import format_links, format_submissions, get_submissions

from dotenv import dotenv_values


config = dotenv_values(".env")


def greg_daemon(local_handler):
    """Aggregates and formats new incoming submissions given subreddits."""

    logging.debug("Getting subreddits...")
    subreddits = get_subreddits()
    logging.debug(f"Detected {len(subreddits)} subreddits.")

    logging.debug("Getting submissions...")
    submissions = get_submissions(subreddits)

    logging.info(f"Detected {len(submissions)} submissions, processing...")
    formatted_submissions = format_submissions(submissions)
    logging.debug("Formatting links...")
    formatted_links = format_links(submissions)

    logging.debug("Posting submissions...")
    s_code = post_submissions(formatted_submissions)
    logging.debug(f"Received HTTP status code {s_code}.")

    logging.debug("Posting links...")
    l_code = post_links(formatted_links)
    logging.debug(f"Received HTTP status code {l_code}.")

    logging.debug(f"Finished aggregation chapter. Sleeping...")
    local_handler.enter(60, 1, greg_daemon, (local_handler,))
