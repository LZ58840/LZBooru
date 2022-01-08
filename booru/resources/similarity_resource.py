from flask import request
import requests
import PIL
from flask_restful import abort
from booru.resources.auth_resource import AuthResource

from booru.database import SIMILARITY_FUNC, db
from tools.encoders import ENCODING_ALGORITHMS
from sqlalchemy import text

from dotenv import dotenv_values

from flask import current_app as app


config = dotenv_values(".env")


SIMILARITY_ENDPOINT = "/api/similarity"
DOWNLOAD_HEADERS = { "User-Agent": config["REDDIT_USER_AGENT"] }


class SimilarityResource(AuthResource):
    """
    A Resource that handles requests related to image similarity.
    """

    def post(self, source=None):
        img_fd = None

        if source == "file":
            img_fd = request.files.get("image")

        elif source == "url":
            url = request.form.get('url')
            response = requests.get(url=url, headers=DOWNLOAD_HEADERS, stream=True)

            if response.status_code == 200:
                img_fd = response.raw

        if img_fd is None:
            app.logger.error(f'"POST {request.full_path}" 400')
            abort(400, message="Invalid file.")
        
        else:
            try:
                q = int(request.args.get('q'))
                algorithm = str(request.args.get('algorithm'))
                encoder = ENCODING_ALGORITHMS[algorithm][1]
                img = encoder(PIL.Image.open(img_fd).convert("RGB").resize((512, 512)))
                m = ENCODING_ALGORITHMS[algorithm][0]

                stmt = SIMILARITY_FUNC.format(
                    alg=algorithm,
                    red="ARRAY"+str(img["red"]) if isinstance(img["red"], list) else f"""B'{img["red"]}'""",
                    green="ARRAY"+str(img["green"]) if isinstance(img["green"], list) else f"""B'{img["green"]}'""",
                    blue="ARRAY"+str(img["blue"]) if isinstance(img["blue"], list) else f"""B'{img["blue"]}'""",
                    model=m,
                    quantity=q
                    )

                query = db.session.execute(text(stmt))

            except Exception as e:
                app.logger.info(f'"POST {request.full_path}" 500')
                abort(500, message="Unexpected Error!")

            else:
                app.logger.info(f'"POST {request.full_path}" 201')

                result = [
                    {
                        "image": image_url,
                        "url": "https://redd.it/" + submission_id,
                        "similarity": float(similarity)
                    }
                    for image_url, submission_id, similarity in query
                    ]

                return result, 201
            
