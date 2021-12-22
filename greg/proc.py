from greg.api import get_subreddit_submissions
from queue import Queue
from threading import Thread


def _get_subreddit_submissions_thread(subreddits_queue, submissions_json):
    while not subreddits_queue.empty():
        i, subreddit_json = subreddits_queue.get()
        submissions_json[i] = get_subreddit_submissions(subreddit_json)
        subreddits_queue.task_done()
    return True


def get_submissions(subreddits_json):
    subreddit_queue = Queue(maxsize=0)
    num_threads = min(50, len(subreddits_json))
    pushshift_submissions_json = [{} for _ in subreddits_json]
    for i in range(len(subreddits_json)):
        subreddit_queue.put((i, subreddits_json[i]))
    for i in range(num_threads):
        worker = Thread(target=_get_subreddit_submissions_thread, args=(subreddit_queue, pushshift_submissions_json))
        worker.setDaemon(True)
        worker.start()
    subreddit_queue.join()
    return pushshift_submissions_json