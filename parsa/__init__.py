from parsa.api import delete_succeeded_links, get_links, post_images, put_failed_links
from parsa.proc import parse_generic_links, parse_imgur_links, parse_reddit_links


REFRESH_DELAY = 60


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
