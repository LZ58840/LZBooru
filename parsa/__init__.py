import logging
from sched import scheduler
from time import time, sleep
from multiprocessing import Process, Queue
from parsa.api import delete_succeeded_links, get_links, post_images, put_failed_links
from parsa.log_queue import listener_process, worker_config
from parsa.proc import parse_generic_links, parse_imgur_links, parse_reddit_links

from dotenv import dotenv_values


config = dotenv_values(".env")


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


def parsa_daemon(local_handler, link_type, parser_config, logger):
    """Obtains and converts given links into direct images."""

    logger.debug(f"Getting {link_type} links...")
    links = get_links(link_type, parser_config["quantity"])
    logger.debug(f"Detected {len(links)} links.")

    logger.debug(f"Parsing {link_type} links...")
    result = parser_config["parser"](links)
    logger.info(f'Parsed {link_type} links ({len(result["succeeded"])} processed, {len(result["failed"])} failed)')

    logger.debug(f"Posting {link_type} images...")
    i_code = post_images(result["images"])
    logger.debug(f"Received HTTP status code {i_code}.")

    logger.debug(f"Clearing successful {link_type} links...")
    d_code = delete_succeeded_links(result["succeeded"])
    logger.debug(f"Received HTTP status code {d_code}.")

    logger.debug(f"Updating failed {link_type} links...")
    f_code = put_failed_links(result["failed"])
    logger.debug(f"Received HTTP status code {f_code}.")

    logger.debug(f"Finished {link_type} parsing chapter. Sleeping...")
    local_handler.enter(parser_config["refresh_delay"], 1, parsa_daemon, (local_handler, link_type, parser_config, logger))


def run_daemon(link_type, parser_config, logging_queue):
    """Schedules and starts the parser daemon."""
    
    worker_config(logging_queue)
    worker_logger = logging.getLogger(link_type)

    handler = scheduler(time, sleep)
    handler.enter(0, 1, parsa_daemon, (handler, link_type, parser_config, worker_logger))
    handler.run()


def run_all():
    """Runs parsers in separate processes."""
    queue = Queue(-1)
    listener = Process(target=listener_process, args=(queue,))
    listener.start()

    worker_config(queue)
    main_logger = logging.getLogger('main')

    processes = []
    for link_type, parser_config in parser_configs.items():
        p = Process(target=run_daemon, args=(link_type, parser_config, queue))
        processes.append(p)
        p.start()
        main_logger.info(f"Created {link_type} parser.")

    main_logger.info("Joining parsers...")
    for p in processes:
        p.join()

