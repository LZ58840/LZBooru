import requests
import re
import logging
from json.decoder import JSONDecodeError
from prawcore.exceptions import Forbidden
from time import sleep
from datetime import datetime, timezone
from dotenv import dotenv_values
from api import praw_api
from parsa.patterns import *
from parsa.urls import *
from requests.exceptions import MissingSchema


config = dotenv_values(".env")
BOORU_URL = config["URL"]
BOORU_HEADERS = { "x-api-key": config["API_KEY"] }
IMGUR_HEADERS = { "Authorization": f"Client-ID {config['IMGUR_CLIENT_ID']}" }


def get_links(link_type, quantity):
    """
    Obtains a list of links of link_type.

    :param link_type: type of link to get
    :param quantity: max number of links to get
    :return: JSON formatted dict of Link entries
    """

    links_json = requests.get(url=f"{BOORU_URL}/link/{link_type}?q={quantity}", headers=BOORU_HEADERS).json()

    return links_json


def parse_reddit_link(link_json):
    """
    Parses a reddit link as Image.

    :param link_json: JSON formatted dict of a Link entry
    :return: relative dict slice (images, succeeded, failed)
    """

    url = link_json["url"]
    reddit_capture = re.match(REDDIT_PATTERN, url)

    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }
    parsed_images = []

    if (img_id := reddit_capture.group('imgid')) is not None:
        # Single image, just append image URL
        parsed_images.append(f"{REDDIT_IMAGE_URL}/{img_id}")
        result["succeeded"].append(link_json)
    
    elif (gallery_id := reddit_capture.group('galleryid')) is not None:
        # Gallery of images, access submission to obtain images
        try:
            submission = praw_api.submission(gallery_id)
            parsed_images.extend([f"{REDDIT_IMAGE_URL}/{item['media_id']}.{submission.media_metadata[item['media_id']]['m'].split('/')[1]}" for item in submission.gallery_data["items"]])
            result["succeeded"].append(link_json)

        except (AttributeError, TypeError, Forbidden):
            # Mark 404 and 403 request errors as failed
            result["failed"].append(link_json)

    result["images"] = [
        {
            "submission_id" : link_json["id"],
            "url"           : parsed_link
        }
        for parsed_link in parsed_images
    ]

    return result


def parse_imgur_link(link_json):
    """
    Parses an imgur link as Image.

    :param link_json: JSON formatted dict of a Link entry
    :return: relative dict slice (images, succeeded, failed)
    """

    url = link_json["url"]
    imgur_capture = re.match(IMGUR_PATTERN, url)

    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }
    parsed_images = []

    request_url = None

    if (img_id := imgur_capture.group('imgid')) not in [None, '', '0']:
        # Set to image endpoint
        request_url = f"{IMGUR_URL}/image/{img_id}"

    elif (album_id := imgur_capture.group('albumid')) is not None:
        # Set to album endpoint
        request_url = f"{IMGUR_URL}/album/{album_id}/images"

    elif (gallery_id := imgur_capture.group('galleryid')) is not None:
        # Set to gallery endpoint
        request_url = f"{IMGUR_URL}/gallery/{gallery_id}/images"
    
    try:
        sleep(8)  # Avg rate-limit interval
        response = requests.get(url=request_url, headers=IMGUR_HEADERS)
        
        if response.status_code != 200:
            result["failed"].append(link_json)
        
        else:
            response_json = response.json()

            if img_id not in [None, '', '0']:
                # Single image, just append URL
                parsed_images.append(response_json["data"]["link"])
            
            elif album_id is not None or gallery_id is not None:
                # Album or gallery of images
                if isinstance(response_json["data"], list):
                    # Album/gallery has more than one image
                    parsed_images.extend([image_json["link"] for image_json in response_json["data"]])

                else:
                    # Album/gallery has only one image
                    parsed_images.append(response_json["data"]["link"])

            result["succeeded"].append(link_json)

    except (JSONDecodeError, KeyError, MissingSchema):
        result["failed"].append(link_json)

    finally:
        result["images"] = [
            {
                "submission_id" : link_json["id"],
                "url"           : parsed_link
            }
            for parsed_link in parsed_images
        ]

        return result


def parse_generic_link(link_json):
    """
    Parses a generic link as Image.

    :param link_json: JSON formatted dict of a Link entry
    :return: relative dict slice (images, succeeded, failed)
    """

    return {
        "images": [
            {
                "submission_id" : link_json["id"],
                "url"           : link_json["url"]
            }
        ],
        "succeeded": [link_json],
        "failed": []
    }


def delete_succeeded_links(links_json):
    """
    Deletes links that were successfully parsed.

    :param links_json: JSON formatted dict of Link entries
    :return: status code
    """

    payload = links_json
    response = requests.delete(url=f"{BOORU_URL}/link", json=payload, headers=BOORU_HEADERS)

    return response.status_code


def put_failed_links(links_json):
    """
    Updates links that failed to parse.

    :param links_json: JSON formatted dict of Link entries
    :return: status code
    """

    for link_json in links_json:
        # Increment priority of each link by 1
        link_json["last_visited"] = int(datetime.now(timezone.utc).timestamp())
        link_json["priority"] += 1

    payload = links_json
    response = requests.put(url=f"{BOORU_URL}/link", json=payload, headers=BOORU_HEADERS)

    return response.status_code


def post_images(images_json):
    """
    Uploads generated Images.

    :param images_json: JSON formatted dict of Image entries
    :return: status code
    """

    payload = images_json
    response = requests.post(url=f"{BOORU_URL}/image", json=payload, headers=BOORU_HEADERS)

    return response.status_code
