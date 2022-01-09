from multiprocessing import Pool, cpu_count
from queue import Queue
from threading import Thread
from parsa.api import parse_imgur_link, parse_reddit_link, parse_generic_link


def _parse_reddit_link_thread(links_queue, results):
    while not links_queue.empty():
        link_json = links_queue.get()
        results.append(parse_reddit_link(link_json))
        links_queue.task_done()
    return True


def parse_reddit_links(links_json):
    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }

    links_queue = Queue(maxsize=0)
    num_threads = min(10, len(links_json))
    rets = []
    for i in range(len(links_json)):
        links_queue.put(links_json[i])
    for _ in range(num_threads):
        image_worker = Thread(target=_parse_reddit_link_thread, args=(links_queue, rets))
        image_worker.setDaemon(True)
        image_worker.start()
    links_queue.join()

    for ret in rets:
        result = {key: value + ret[key] for key, value in result.items()}

    return result


def parse_imgur_links(links_json):
    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }

    for link_json in links_json:
        ret = parse_imgur_link(link_json)
        result = {key: value + ret[key] for key, value in result.items()}

    return result
    

def parse_generic_links(links_json):
    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }

    pool = Pool(cpu_count() - 1)
    rets = pool.map(parse_generic_link, links_json)
    for ret in rets:
        result = {key: value + ret[key] for key, value in result.items()}

    return result
