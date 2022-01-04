from json.decoder import JSONDecodeError
from time import sleep
import requests
from dotenv import dotenv_values
import re
from booru.api import reddit


config = dotenv_values(".env")

PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search"
IMGUR_URL = "https://api.imgur.com/3"
REDDIT_GALLERY_URL = "https://www.reddit.com/comments"
REDDIT_IMAGE_URL = "https://i.redd.it"
DEVIANTART_URL = "https://backend.deviantart.com/oembed"
IMGUR_HEADERS = { "Authorization": f"Client-ID {config['IMGUR_CLIENT_ID']}" }


IMGUR_IMAGE_RE = r"(^(http|https):\/\/)?(i\.)?imgur.com\/((?P<gallery>gallery\/)(?P<galleryid>\w+)|(?P<album>a\/)(?P<albumid>\w+)#?)?(?P<imgid>\w*)"
IMGUR_GARBAGE = ['', '0']
REDDIT_IMAGE_RE = r"(^(http|https):\/\/)?(((i|preview)\.redd\.it\/)(?P<imgid>\w+\.\w+)|(www\.reddit\.com\/gallery\/)(?P<galleryid>\w+))"
ANY_IMAGE_RE = r"(https?:\/\/.*\.(?:png|jpg|jpeg))"
DEVIANTART_RE = r"^(.+).deviantart.com(.+?)(\?.*?q=(\w+))?$"


def _try_get(**kwargs):
    timeout = 10
    multiplier = 2
    tries = 3
    for _ in range(tries):
        result = requests.get(**kwargs)
        status_code = result.status_code
        if status_code == 200:
            return result
        elif status_code in [401, 403, 404]:
            return None
        else:  # status_code in [429, 503, 504]:
            sleep(timeout)
            timeout *= multiplier
            continue
    return None


def _get_imgur_urls(parent_url):
    """Error checking not implemented here. Assume external functions work correctly."""
    imgur_capture = re.match(IMGUR_IMAGE_RE, parent_url)

    try:
        if (img_id := imgur_capture.group('imgid')) is not None and img_id not in IMGUR_GARBAGE:
            # single image link
            result = _try_get(url=f"{IMGUR_URL}/image/{img_id}", headers=IMGUR_HEADERS)
            result_json = result.json()
            return [result_json["data"]["link"]]

        elif (album_id := imgur_capture.group('albumid')) is not None:
            # album link
            result = _try_get(url=f"{IMGUR_URL}/album/{album_id}/images", headers=IMGUR_HEADERS)
            result_json = result.json()
            return [image_json["link"] for image_json in result_json["data"]]

        elif (gallery_id := imgur_capture.group('galleryid')) is not None:
            # gallery link
            result = _try_get(url=f"{IMGUR_URL}/gallery/{gallery_id}/images", headers=IMGUR_HEADERS)
            result_json = result.json()
            return [image_json["link"] for image_json in result_json["data"]]

        else:
            return []

    except JSONDecodeError:
        print(f"unable to obtain {parent_url} (wrong json). broken link?")
        print(result.status_code)
        return []
    
    except KeyError:
        print(f"unable to obtain {parent_url} (wrong key). broken link?")
        print(result.status_code)
        return []

    except TypeError:
        print(f"unable to obtain {parent_url} (wrong type). broken link?")
        print(result.status_code)
        return []

    except AttributeError:
        return []


def _get_reddit_urls(parent_url):
    """Error checking not implemented here. Assume external functions work correctly."""
    reddit_capture = re.match(REDDIT_IMAGE_RE, parent_url)
    result = None

    try: 
        if (img_id := reddit_capture.group('imgid')) is not None:
            # single image link
            return [f"{REDDIT_IMAGE_URL}/{img_id}"]

        elif (gallery_id := reddit_capture.group('galleryid')) is not None:
            # gallery link
            result = reddit.submission(gallery_id)
            return [f"{REDDIT_IMAGE_URL}/{item['media_id']}.{result.media_metadata[item['media_id']]['m'].split('/')[1]}" for item in result.gallery_data["items"]]

        # elif (gallery_id := reddit_capture.group('galleryid')) is not None:
        #     # gallery link
        #     PARAMS = { "ids": gallery_id }
        #     result = requests.get(url=f"{PUSHSHIFT_URL}/submissions", params=PARAMS)
        #     result_json = result.json()["data"][0]
        #     return [f"{REDDIT_IMAGE_URL}/{item['media_id']}.{result_json['media_metadata'][item['media_id']]['m'].split('/')[1]}" for item in result_json["gallery_data"]["items"]]

        else:
            return []
    
    except JSONDecodeError:
        print(f"unable to obtain {parent_url} (wrong json). broken link?")
        return []
    
    except KeyError:
        print(f"unable to obtain {parent_url} (wrong key). broken link?")
        return []

    except TypeError:
        print(f"unable to obtain {parent_url} (wrong type). broken link?")
        return []

    except AttributeError:
        return []


def _get_deviantart_urls(parent_url):
    try:
        PARAMS = { "url": parent_url }
        result_json = _try_get(url=DEVIANTART_URL, params=PARAMS).json()
        return [result_json["url"]]
    
    except JSONDecodeError:
        print(f"unable to obtain {parent_url}. broken link?")
        return []
    
    except KeyError:
        print(f"unable to obtain {parent_url}. broken link?")
        return []

    except TypeError:
        print(f"unable to obtain {parent_url}. broken link?")
        return []


def _get_generic_urls(parent_url):
    """Error checking not implemented here. Assume external functions work correctly."""
    return [parent_url]


def get_image_urls(parent_url):
    if re.match(IMGUR_IMAGE_RE, parent_url) is not None:
        return _get_imgur_urls(parent_url)

    elif re.match(REDDIT_IMAGE_RE, parent_url) is not None:
        return _get_reddit_urls(parent_url)

    # elif re.match(DEVIANTART_RE, parent_url) is not None:
    #     return _get_deviantart_urls(parent_url)

    elif re.match(ANY_IMAGE_RE, parent_url) is not None:
        return _get_generic_urls(parent_url)

    else:
        return []
