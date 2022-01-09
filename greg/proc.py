from greg.api import get_subreddit_submissions_json
from greg.format import format_link_json, format_submission_json
from queue import Queue
from threading import Thread
from multiprocessing import cpu_count, Pool


def get_submissions(subreddits_json):
    submissions_json = []
    for subreddit_json in subreddits_json:
        subreddit_submissions_json = get_subreddit_submissions_json(subreddit_json)
        submissions_json.extend(subreddit_submissions_json)
    return submissions_json


def format_submissions(submissions_json):
    pool = Pool(cpu_count() - 1)
    formatted_submissions_json = pool.map(format_submission_json, submissions_json)
    return formatted_submissions_json


def _format_link_json_thread(links_queue, links_json):
    while not links_queue.empty():
        submission_json = links_queue.get()
        links_json.append(format_link_json(submission_json))
        links_queue.task_done()
    return True


def format_links(submissions_json):
    links_queue = Queue(maxsize=0)
    num_threads = min(10, len(submissions_json))
    links_json = []
    for i in range(len(submissions_json)):
        links_queue.put(submissions_json[i])
    for _ in range(num_threads):
        link_worker = Thread(target=_format_link_json_thread, args=(links_queue, links_json))
        link_worker.setDaemon(True)
        link_worker.start()
    links_queue.join()
    return links_json
