from json.decoder import JSONDecodeError
import requests
from datetime import datetime, timedelta
from dotenv import dotenv_values
import re


config = dotenv_values(".env")
BOORU_URL = config["URL"]
PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search"
IMGUR_URL = "https://api.imgur.com/3"
REDDIT_GALLERY_URL = "https://www.reddit.com/comments"
REDDIT_IMAGE_URL = "https://i.redd.it/"
BOORU_HEADERS = { "x-api-key": config["API_KEY"] }
IMGUR_HEADERS = { "Authorization": f"Client-ID {config['IMGUR_CLIENT_ID']}" }


IMGUR_IMAGE_RE = r"(^(http|https):\/\/)?(i\.)?imgur.com\/((?P<gallery>gallery\/)(?P<galleryid>\w+)|(?P<album>a\/)(?P<albumid>\w+)#?)?(?P<imgid>\w*)"
REDDIT_IMAGE_RE = r"(^(http|https):\/\/)?(((i|preview)\.redd\.it\/)(?P<imgid>\w+\.\w+)|(www\.reddit\.com\/gallery\/)(?P<galleryid>\w+))"
ANY_IMAGE_RE = r"(https?:\/\/.*\.(?:png|jpg|jpeg))"


def get_subreddits():
    subreddits_json = requests.get(url=f"{BOORU_URL}/subreddit", headers=BOORU_HEADERS).json()
    return subreddits_json


def get_subreddit_submissions_json(subreddit_json):
    after_utc = subreddit_json["updated"] if subreddit_json["updated"] is not None else subreddit_json["created"]
    after_datetime = datetime.utcfromtimestamp(after_utc)
    after = after_datetime.strftime('%Y-%m-%d')
    before = (after_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
    PARAMS = {
        "subreddit": subreddit_json["name"],
        "after": after,
        "before": before,
        "size": 500
    }

    submissions_json = requests.get(url=f"{PUSHSHIFT_URL}/submission", params=PARAMS).json()
    return submissions_json["data"]


def update_subreddits(subreddits_json):
    for subreddit_json in subreddits_json:
        updated_utc = subreddit_json["updated"] if subreddit_json["updated"] is not None else subreddit_json["created"]
        subreddit_json["updated"] = int((datetime.utcfromtimestamp(updated_utc) + timedelta(days=1)).timestamp())
    payload = subreddits_json
    return requests.put(url=f"{BOORU_URL}/subreddit", json=payload, headers=BOORU_HEADERS)


def post_images(formatted_images_json):
    payload = formatted_images_json
    return requests.post(url=f"{BOORU_URL}/image", json=payload, headers=BOORU_HEADERS)


def post_submissions(formatted_submissions_json):
    payload = formatted_submissions_json
    return requests.post(url=f"{BOORU_URL}/submission", json=payload, headers=BOORU_HEADERS)


def _get_imgur_urls(parent_url):
    """Error checking not implemented here. Assume external functions work correctly."""
    imgur_capture = re.match(IMGUR_IMAGE_RE, parent_url)

    try:
        if (img_id := imgur_capture.group('imgid')) is not None and img_id != '':
            # single image link
            result = requests.get(url=f"{IMGUR_URL}/image/{img_id}", headers=IMGUR_HEADERS)
            result_json = result.json()
            return [result_json["data"]["link"]]

        elif (album_id := imgur_capture.group('albumid')) is not None:
            # album link
            result = requests.get(url=f"{IMGUR_URL}/album/{album_id}/images", headers=IMGUR_HEADERS)
            result_json = result.json()
            return [image_json["link"] for image_json in result_json["data"]]

        elif (gallery_id := imgur_capture.group('galleryid')) is not None:
            # gallery link
            result = requests.get(url=f"{IMGUR_URL}/gallery/{gallery_id}/images", headers=IMGUR_HEADERS)
            result_json = result.json()
            return [image_json["link"] for image_json in result_json["data"]]

        else:
            return []

    except JSONDecodeError:
        return []


def _get_reddit_urls(parent_url):
    """Error checking not implemented here. Assume external functions work correctly."""
    reddit_capture = re.match(REDDIT_IMAGE_RE, parent_url)

    if (img_id := reddit_capture.group('imgid')) is not None:
        # single image link
        return [f"{REDDIT_IMAGE_URL}/{img_id}"]

    elif (gallery_id := reddit_capture.group('galleryid')) is not None:
        # gallery link
        PARAMS = { "ids": gallery_id }
        result_json = requests.get(url=f"{PUSHSHIFT_URL}/submissions", params=PARAMS).json()["data"][0]
        return [f"{REDDIT_IMAGE_URL}/{item['media_id']}.{result_json['media_metadata'][item['media_id']]['m'].split('/')[1]}" for item in result_json["gallery_data"]["items"]]

    else:
        return []


def _get_generic_urls(parent_url):
    """Error checking not implemented here. Assume external functions work correctly."""
    return [parent_url]


def get_image_urls(parent_url):
    if re.match(IMGUR_IMAGE_RE, parent_url) is not None:
        return _get_imgur_urls(parent_url)

    elif re.match(REDDIT_IMAGE_RE, parent_url) is not None:
        return _get_reddit_urls(parent_url)

    elif re.match(ANY_IMAGE_RE, parent_url) is not None:
        return _get_generic_urls(parent_url)

    else:
        return []


def format_submission_json(submission_json):
    return {
        "id": submission_json["id"],
        "title": submission_json["title"],
        "author": submission_json["author"],
        "subreddit": submission_json["subreddit"],
        "created": submission_json["created_utc"],
        "flair": submission_json["link_flair_text"] if "link_flair_text" in submission_json else None,
        "nsfw": submission_json["over_18"]
    }


def format_image_json(submission_json):
    image_urls = get_image_urls(submission_json["url"])
    return [{"url": image_url, "submission_id": submission_json["id"]} for image_url in image_urls]

