import multiprocessing as mp
import queue
from threading import Thread
from tools.encoders import ENCODING_FUNCTIONS

from coco.download import download_image
from coco.encode import encode_image


def _download_image_thread(images_queue, results):
    while not images_queue.empty():
        image_json = images_queue.get()
        results.append(download_image(image_json))
        images_queue.task_done()
    return True


def download_images(images_json):
    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }
    images_queue = queue.Queue(maxsize=0)
    num_threads = min(10, len(images_json))
    rets = []
    for i in range(len(images_json)):
        images_queue.put(images_json[i])
    for _ in range(num_threads):
        image_worker = Thread(target=_download_image_thread, args=(images_queue, rets))
        image_worker.setDaemon(True)
        image_worker.start()
    images_queue.join()

    for ret in rets:
        result = {key: value + ret[key] for key, value in result.items()}

    return result


def _encode_image_wrapper(args):
    return encode_image(*args)


def _encode_image(img_tuples, encoder_func):
    pool = mp.Pool(mp.cpu_count() - 1)

    args = [(img_tuple, encoder_func) for img_tuple in img_tuples]

    encoded_json = pool.map(_encode_image_wrapper, args)

    return encoded_json


def encode_images(img_tuples):
    encoded_jsons = {}

    for encoder, encoder_func in ENCODING_FUNCTIONS.items():
        encoded_jsons[encoder] = _encode_image(img_tuples, encoder_func)

    return encoded_jsons
