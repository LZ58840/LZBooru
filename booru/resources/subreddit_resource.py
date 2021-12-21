from flask import request
from flask_restful import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.subreddit import Subreddit
from booru.schemas.subreddit_schema import SubredditSchema

from booru.api.subreddit_api import subreddit_exists, get_subreddit_created


SUBREDDIT_ENDPOINT = "/api/subreddit"


class SubredditResource(AuthResource):
    def get(self, name=None):
        if not name:
            return self._get_all_subreddits(), 200

        try:
            return self._get_subreddit_by_name(name), 200
        except NoResultFound:
            abort(404, message="Subreddit not found.")

    def _get_all_subreddits(self):
        subreddits = Subreddit.query.all()
        subreddits_json = [SubredditSchema().dump(subreddit) for subreddit in subreddits]
        return subreddits_json
    
    def _get_subreddit_by_name(self, name):
        subreddit = Subreddit.query.filter_by(name=name).first()
        subreddit_json = SubredditSchema().dump(subreddit)

        if not subreddit_json:
            raise NoResultFound()
        
        return subreddit_json

    def post(self):
        subreddit_json = request.get_json()
        subreddit_name = subreddit_json["name"]

        if not subreddit_exists(subreddit_name):
            abort(400, message=f"Subreddit {subreddit_name} does not exist!")
        else:
            subreddit_json["created"] = get_subreddit_created(subreddit_name)
            subreddit = SubredditSchema().load(subreddit_json)

            try:
                db.session.add(subreddit)
                db.session.commit()
            except IntegrityError as e:
                abort(500, message="Unexpected Error!")
            else:
                return subreddit.name, 201

