from greg.api import format_image_json, get_subreddit_submissions_json, format_submission_json
from queue import Queue
from threading import Thread
from multiprocessing import cpu_count, Pool
import itertools


def _get_subreddit_submissions_thread(subreddits_queue, submissions_json):
    while not subreddits_queue.empty():
        subreddit_json = subreddits_queue.get()
        submissions_json.extend(get_subreddit_submissions_json(subreddit_json))
        subreddits_queue.task_done()
    return True


def get_submissions(subreddits_json):
    subreddit_queue = Queue(maxsize=0)
    num_threads = min(50, len(subreddits_json))
    submissions_json = []
    for i in range(len(subreddits_json)):
        subreddit_queue.put(subreddits_json[i])
    for _ in range(num_threads):
        subreddit_worker = Thread(target=_get_subreddit_submissions_thread, args=(subreddit_queue, submissions_json))
        subreddit_worker.setDaemon(True)
        subreddit_worker.start()
    subreddit_queue.join()
    return submissions_json


def format_submissions(submissions_json):
    pool = Pool(cpu_count() - 1)
    formatted_submissions_json = pool.map(format_submission_json, submissions_json)
    return formatted_submissions_json


def format_images(submissions_json):
    pool = Pool(cpu_count() - 1)
    formatted_image_json = pool.map(format_image_json, submissions_json)
    return list(itertools.chain.from_iterable(formatted_image_json))