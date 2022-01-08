import logging
from coco.api import delete_failed, get_images, post_encoded
from coco.proc import download_images, encode_images

from dotenv import dotenv_values


config = dotenv_values(".env")


def coco_daemon(local_handler):
    """Encodes images in various formats for recognition training."""

    logging.debug("Getting images...")
    images = get_images()
    logging.debug(f"Detected {len(images)} images.")

    logging.debug("Downloading images...")
    result = download_images(images)
    logging.info(f'Downloaded images ({len(result["succeeded"])} downloaded, {len(result["failed"])} failed)')

    logging.debug(f"Encoding images...")
    encoded = encode_images(result["images"])

    logging.debug(f"Posting encoded images...")
    e_code = post_encoded(encoded)
    logging.debug(f"Received HTTP status codes {', '.join(e_code)}.")

    logging.debug(f"Deleting failed images...")
    d_code = delete_failed(result["failed"])
    logging.debug(f"Received HTTP status code {d_code}.")

    logging.debug(f"Finished encoding chapter. Sleeping...")
    local_handler.enter(60, 1, coco_daemon, (local_handler,))
