from flask import request
from flask_restful import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.submission import Submission
from booru.schemas.submission_schema import SubmissionSchema


SUBMISSION_ENDPOINT = "/api/submission"


class SubmissionResource(AuthResource):
    def get(self, url=None):
        if not url:
            return self._get_all_submissions(), 200
        
        try:
            return self._get_by_url(url), 200
        except NoResultFound:
            abort(404, message="Submission not found.")

    def _get_all_submissions(self):
        submissions = Submission.query.all()
        submission_json = [SubmissionSchema().dump(submission) for submission in submissions]
        return submission_json
        
    def _get_by_url(self, url):
        submission = Submission.query.filter_by(url=url).first()
        submission_json = SubmissionSchema().dump(submission)

        if not submission_json:
            raise NoResultFound()

        return submission_json

    def post(self):
        submissions_json = request.get_json()
        submissions = SubmissionSchema(many=True).load(submissions_json)

        try:
            db.session.add_all(submissions)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Unexpected Error!")
        else:
            return len(submissions), 201
