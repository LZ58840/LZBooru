from flask import request
from flask_restful import abort
from sqlalchemy.exc import IntegrityError
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.link import Link
from booru.schemas.link_schema import LinkSchema


LINK_ENDPOINT = "/api/link"


class LinkResource(AuthResource):
    def get(self):
        links = Link.query.all()
        links_json = [LinkSchema().dump(image) for image in links]
        return links_json, 200

    def post(self):
        links = LinkSchema(many=True).load(request.get_json())

        try:
            db.session.add_all(links)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Unexpected Error!")
        else:
            return len(links), 201

