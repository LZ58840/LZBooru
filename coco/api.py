from dotenv import dotenv_values
import requests


config = dotenv_values(".env")
BOORU_URL = config["URL"]
BOORU_HEADERS = { "x-api-key": config["API_KEY"] }
DOWNLOAD_HEADERS = { "User-Agent": config["REDDIT_USER_AGENT"] }


def get_images(quantity=1000):
    """
    Obtains a list of images that have not been encoded by unencoded_type yet.

    :param unencoded_type: encoder that encodes Images
    :param quantity: max number of images to get
    :return: JSON formatted dict of Image entries
    """

    images_json = requests.get(url=f"{BOORU_URL}/image?q={quantity}", headers=BOORU_HEADERS).json()

    return images_json


def post_encoded(encoded_jsons):
    response_codes = {}

    for encoding_type, encoded_json in encoded_jsons.items():
        payload = encoded_json
        response = requests.post(url=f"{BOORU_URL}/{encoding_type}", json=payload, headers=BOORU_HEADERS)
        response_codes[encoding_type] = response.status_code

    return response_codes


def delete_failed(failed_json):
    payload = failed_json
    response = requests.delete(url=f"{BOORU_URL}/image", json=payload, headers=BOORU_HEADERS)

    return response.status_code