from flask import request
from flask_restful import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.link import Link
from booru.schemas.link_schema import LinkSchema
from datetime import datetime, timezone, timedelta

from flask import current_app as app


LINK_ENDPOINT = "/api/link"


class LinkResource(AuthResource):
    def get(self, link_type=None):
        try:
            quantity = int(request.args.get('q'))

        except (ValueError, TypeError):
            app.logger.info(f'"GET {request.full_path}" 400')
            abort(400, message="Invalid quantity.")

        else:
            if not link_type:
                return self._get_links(quantity), 200

            else:
                return self._get_links_by_type(link_type, quantity), 200

    def _get_links(self, quantity):
        hour_threshold = int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp())

        links = Link.query\
            .filter(or_(Link.last_visited.is_(None), Link.last_visited <= hour_threshold))\
            .order_by(Link.priority.asc(), Link.created.asc())\
            .limit(quantity).all()

        links_json = [LinkSchema().dump(image) for image in links]

        app.logger.info(f'"GET {request.full_path}" 200')

        return links_json
    
    def _get_links_by_type(self, link_type, quantity):
        hour_threshold = int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp())

        links = Link.query\
            .filter(Link.type == link_type, 
                    or_(Link.last_visited.is_(None), Link.last_visited <= hour_threshold))\
            .order_by(Link.priority.asc(), Link.created.asc())\
            .limit(quantity).all()

        links_json = [LinkSchema().dump(image) for image in links]

        app.logger.info(f'"GET {request.full_path}" 200')

        return links_json

    def post(self):
        links = LinkSchema(many=True).load(request.get_json())

        try:
            db.session.add_all(links)
            db.session.commit()

        except IntegrityError as e:
            app.logger.exception(f'"POST {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"POST {request.full_path}" 201')
            return len(links), 201

    def delete(self):
        links_json = request.get_json()

        try:
            for link_json in links_json:
                Link.query.filter_by(id=link_json["id"]).delete()
            db.session.commit()

        except IntegrityError as e:
            app.logger.exception(f'"DELETE {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"DELETE {request.full_path}" 200')
            return len(links_json), 200

    def put(self):
        links = LinkSchema(many=True).load(request.get_json())

        try:
            for link in links:
                if link.priority >= 3:
                    Link.query.filter_by(id=link.id).delete()

                else:
                    db.session.merge(link)

            db.session.commit()

        except IntegrityError as e:
            app.logger.exception(f'"PUT {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"PUT {request.full_path}" 200')
            return len(links), 200
