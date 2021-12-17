from marshmallow import Schema, fields, post_load
from booru.models.submission import Submission


class SubmissionSchema(Schema):
    id = fields.Integer()
    url = fields.String(allow_none=False)
    title = fields.String(allow_none=False)
    contributor = fields.Integer(allow_none=False)
    subreddit = fields.Integer(allow_none=False)
    created = fields.DateTime(allow_none=False)
    flair = fields.String(allow_none=False)
    image = fields.Integer(allow_none=False)
    nsfw = fields.Boolean()
    removed = fields.Boolean()

    @post_load
    def make_submission(self, data, **kwargs):
        return Submission(**data)
