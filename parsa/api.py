from json.decoder import JSONDecodeError
from prawcore.exceptions import Forbidden
import requests
import re
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
    links_json = requests.get(url=f"{BOORU_URL}/link/{link_type}?q={quantity}", headers=BOORU_HEADERS).json()
    return links_json


def parse_reddit_link(link_json):
    url = link_json["url"]
    print(f"processing {url}...")
    reddit_capture = re.match(REDDIT_PATTERN, url)
    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }
    parsed_images = []

    if (img_id := reddit_capture.group('imgid')) is not None:
        parsed_images.append(f"{REDDIT_IMAGE_URL}/{img_id}")
        result["succeeded"].append(link_json)
        print(f"added images from {url}.")
    
    elif (gallery_id := reddit_capture.group('galleryid')) is not None:
        try:
            submission = praw_api.submission(gallery_id)
            parsed_images.extend([f"{REDDIT_IMAGE_URL}/{item['media_id']}.{submission.media_metadata[item['media_id']]['m'].split('/')[1]}" for item in submission.gallery_data["items"]])
            result["succeeded"].append(link_json)
            print(f"added images from {url}.")

        except (AttributeError, TypeError):
            result["failed"].append(link_json)
            print(f"unable to obtain {url} due to incompatibility.")

        except Forbidden:
            result["failed"].append(link_json)
            print(f"unable to obtain {url} due to possible rate limiting.")

    result["images"] = [
        {
            "submission_id" : link_json["id"],
            "url"           : parsed_link
        }
        for parsed_link in parsed_images
    ]
    return result


def parse_imgur_link(link_json):
    url = link_json["url"]
    print(f"processing {url}...")
    imgur_capture = re.match(IMGUR_PATTERN, url)
    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }
    parsed_images = []
    request_url = None
    sleep(8)

    if (img_id := imgur_capture.group('imgid')) not in [None, '', '0']:
        request_url = f"{IMGUR_URL}/image/{img_id}"

    elif (album_id := imgur_capture.group('albumid')) is not None:
        request_url = f"{IMGUR_URL}/album/{album_id}/images"

    elif (gallery_id := imgur_capture.group('galleryid')) is not None:
        request_url = f"{IMGUR_URL}/gallery/{gallery_id}/images"
    
    try:
        response = requests.get(url=request_url, headers=IMGUR_HEADERS)
        
        if response.status_code != 200:
            result["failed"].append(link_json)
            print(f"unable to obtain {url} with response code {response.status_code}.")
        
        else:
            response_json = response.json()

            if img_id not in [None, '', '0']:
                parsed_images.append(response_json["data"]["link"])
            
            elif album_id is not None or gallery_id is not None:
                if isinstance(response_json["data"], list):
                    parsed_images.extend([image_json["link"] for image_json in response_json["data"]])
                else:  # single image 
                    parsed_images.append(response_json["data"]["link"])

            result["succeeded"].append(link_json)
            print(f"added images from {url}.")

    except (JSONDecodeError, KeyError, MissingSchema):
        result["failed"].append(link_json)
        print(f"unable to obtain {url} due to incompatibility.")

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
    payload = links_json
    return requests.delete(url=f"{BOORU_URL}/link", json=payload, headers=BOORU_HEADERS)


def put_failed_links(links_json):
    for link_json in links_json:
        link_json["last_visited"] = int(datetime.now(timezone.utc).timestamp())
        link_json["priority"] += 1
    payload = links_json
    return requests.put(url=f"{BOORU_URL}/link", json=payload, headers=BOORU_HEADERS)


def post_images(images_json):
    payload = images_json
    return requests.post(url=f"{BOORU_URL}/image", json=payload, headers=BOORU_HEADERS)
