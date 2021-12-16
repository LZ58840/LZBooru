from marshmallow import Schema, fields, post_load
from booru.models.submission import Submission


class SubmissionSchema(Schema):
    link_id = fields.String()
    title = fields.String(allow_none=False)
    created = fields.DateTime(allow_none=False)
    flair = fields.String(allow_none=False)
    img = fields.String(allow_none=False)
    removed = fields.Boolean()

    @post_load
    def make_submission(self, data, **kwargs):
        return Submission(**data)
