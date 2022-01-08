from flask import request
from flask_restful import abort
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from booru.resources.auth_resource import AuthResource

from booru.database import db
from booru.models.submission import Submission
from booru.schemas.submission_schema import SubmissionSchema

from flask import current_app as app


SUBMISSION_ENDPOINT = "/api/submission"


class SubmissionResource(AuthResource):
    def get(self, url=None):
        if not url:
            return self._get_all_submissions(), 200
        
        try:
            return self._get_by_url(url), 200

        except NoResultFound:
            app.logger.error(f'"GET {request.full_path}" 404')
            abort(404, message="Submission not found.")

    def _get_all_submissions(self):
        submissions = Submission.query.all()
        submission_json = [SubmissionSchema().dump(submission) for submission in submissions]

        app.logger.info(f'"GET {request.full_path}" 200')

        return submission_json
        
    def _get_by_url(self, url):
        submission = Submission.query.filter_by(url=url).first()
        submission_json = SubmissionSchema().dump(submission)

        if not submission_json:
            raise NoResultFound()

        app.logger.info(f'"GET {request.full_path}" 200')

        return submission_json

    def post(self):
        submissions_json = request.get_json()
        submissions = SubmissionSchema(many=True).load(submissions_json)

        try:
            for submission in submissions:
                db.session.merge(submission)
            db.session.commit()

        except Exception as e:
            app.logger.exception(f'"POST {request.full_path}" 500')
            abort(500, message="Unexpected Error!")

        else:
            app.logger.info(f'"POST {request.full_path}" 201')
            return len(submissions), 201
