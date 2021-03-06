from marshmallow import Schema, fields, post_load
from booru.models.submission import Submission


class SubmissionSchema(Schema):
    """
    A Schema representing a Submission in the LZBooru database.
    """

    id = fields.String()
    title = fields.String(allow_none=False)
    author = fields.String(allow_none=False)
    subreddit = fields.String(allow_none=False)
    created = fields.Integer(allow_none=False)
    flair = fields.String(allow_none=True)
    nsfw = fields.Boolean()

    @post_load
    def make_submission(self, data, **kwargs):
        return Submission(**data)
