from dotenv import dotenv_values
from PIL import Image
import requests


config = dotenv_values(".env")
DOWNLOAD_HEADERS = { "User-Agent": config["REDDIT_USER_AGENT"] }


def download_image(image_json, width=512, height=512):
    url = image_json["url"]

    result = {
        "images": [],
        "succeeded": [],
        "failed": []
    }

    try:
        response = requests.get(url=url, headers=DOWNLOAD_HEADERS, stream=True)

        if response.status_code != 200:
            result["failed"].append(image_json)

        else:
            img = Image.open(response.raw).convert("RGB").resize((width, height))

            result["images"].append((image_json["id"], img))
            result["succeeded"].append(image_json)
    
    except Exception as e:
        result["failed"].append(image_json)
    
    finally:
        return result
