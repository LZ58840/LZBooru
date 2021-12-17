from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from booru.database import db
from booru.models.contributor import Contributor
from booru.schemas.contributor_schema import ContributorSchema


CONTRIBUTOR_ENDPOINT = "/api/contributor"


class ContributorResource(Resource):
    def get(self, name=None):
        if not name:
            return self._get_all_contributors(), 200

        try:
            return self._get_contributor_by_name(name), 200
        except NoResultFound:
            abort(404, message="Contributor not found.")
    
    def _get_all_contributors(self):
        contributors = Contributor.query.all()
        contributors_json = [ContributorSchema().dump(contributor) for contributor in contributors]
        return contributors_json
    
    def _get_contributor_by_name(self, name):
        contributor = Contributor.query.filter_by(name=name).first()
        contributor_json = ContributorSchema().dump(contributor)

        if not contributor_json:
            raise NoResultFound()
        
        return contributor_json

    def post(self):
        contributor = ContributorSchema().load(request.get_json())

        try:
            db.session.add(contributor)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Unexpected Error!")
        else:
            return contributor.id, 201

