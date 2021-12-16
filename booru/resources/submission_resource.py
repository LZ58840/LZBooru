from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from booru.database import db
from booru.models.submission import Submission
from booru.schemas.submission_schema import SubmissionSchema

SUBMISSION_ENDPOINT = "/api/submission"

class SubmissionResource(Resource):
    def get(self, id=None):
        if not id:
            flair = request.args.get("flair")
            return self._get_by_flair(flair), 200
        
        try:
            return self._get_by_id(id), 200
        except NoResultFound:
            abort(404, message="Submission not found")
        
    def _get_by_flair(self, flair):
        submissions = Submission.query.filter_by(flair=flair).all()
        submissions_json = [SubmissionSchema().dump(submissions) for submission in submissions]
        return submissions_json

    def _get_by_id(self, link_id):
        submission = Submission.query.filter_by(link_id=link_id).first()
        submission_json = SubmissionSchema().dump(submission)
        
        if not submission_json:
            raise NoResultFound()

        return submission_json

    def post(self):
        submission = SubmissionSchema().load(request.get_json())

        try:
            db.session.add(submission)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Unexpected Error!")
        else:
            return submission.link_id, 201
