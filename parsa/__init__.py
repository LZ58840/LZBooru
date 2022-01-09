from os import link
from sched import scheduler
from time import time, sleep
from multiprocessing import Process
from parsa.api import delete_succeeded_links, get_links, post_images, put_failed_links
from parsa.proc import parse_generic_links, parse_imgur_links, parse_reddit_links


REFRESH_DELAY = 60


parser_configs = {
    "imgur": {
        "parser": parse_imgur_links,
        "quantity": 1000,
        "refresh_delay": 10
    },
    "reddit": {
        "parser": parse_reddit_links,
        "quantity": 1000,
        "refresh_delay": 60
    },
    "generic": {
        "parser": parse_generic_links,
        "quantity": 1000,
        "refresh_delay": 10
    }
}


def ParsaDaemon(local_handler, link_type, parser_config):
    links = get_links(link_type, parser_config["quantity"])
    result = parser_config["parser"](links)
    post_images(result["images"])
    delete_succeeded_links(result["succeeded"])
    put_failed_links(result["failed"])
    local_handler.enter(parser_config["refresh_delay"], 1, ParsaDaemon, (local_handler, link_type, parser_config))


# def ParsaDaemon(local_handler, parser, link_type, quantity):
#     links = get_links(link_type, quantity)
#     result = parser(links)
#     post_images(result["images"])
#     delete_succeeded_links(result["succeeded"])
#     put_failed_links(result["failed"])
#     local_handler.enter(REFRESH_DELAY, 1, ParsaDaemon, (local_handler, parser, link_type, quantity))


def run_daemon(link_type, parser_config):
    handler = scheduler(time, sleep)
    handler.enter(0, 1, ParsaDaemon, (handler, link_type, parser_config))
    handler.run()


def run_all():
    processes = []
    for link_type, parser_config in parser_configs.items():
        p = Process(target=run_daemon, args=(link_type, parser_config))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    


    # a = Process(target=run_daemon, args=(parse_imgur_links, "imgur", 10))
    # b = Process(target=run_daemon, args=(parse_reddit_links, "reddit", 100))
    # c = Process(target=run_daemon, args=(parse_generic_links, "generic", 1000))
    # a.start()
    # b.start()
    # c.start()
    # a.join()
    # b.join()
    # c.join()


def ParsaImgurDaemon(local_handler):
    # get the earliest BUFFER_SIZE posts with no last_visited and 1 hour or more last_visited
    links = get_links("imgur", 10)
    # attempt to extract direct links, receive json of succeeded and failed
    result = parse_imgur_links(links)
    # post direct links to /image, delete succeeded from /link
    post_images(result["images"])
    delete_succeeded_links(result["succeeded"])
    # update failed links to /link
    put_failed_links(result["failed"])
    local_handler.enter(REFRESH_DELAY, 1, ParsaImgurDaemon, (local_handler,))


def ParsaRedditDaemon(local_handler):
    links = get_links("reddit", 100)
    result = parse_reddit_links(links)
    # post direct links to /image, delete succeeded from /link
    post_images(result["images"])
    delete_succeeded_links(result["succeeded"])
    # update failed links to /link
    put_failed_links(result["failed"])
    local_handler.enter(REFRESH_DELAY, 1, ParsaRedditDaemon, (local_handler,))
    

def ParsaGenericDaemon(local_handler):
    links = get_links("generic", 1000)
    result = parse_generic_links(links)
    # post direct links to /image, delete succeeded from /link
    post_images(result["images"])
    delete_succeeded_links(result["succeeded"])
    # update failed links to /link
    put_failed_links(result["failed"])
    local_handler.enter(REFRESH_DELAY, 1, ParsaGenericDaemon, (local_handler,))
