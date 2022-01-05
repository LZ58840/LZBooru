from marshmallow import Schema, fields, post_load
from booru.models.subreddit import Subreddit


class SubredditSchema(Schema):
    """
    A Schema representing a Subreddit in the LZBooru database.
    """

    name = fields.String()
    created = fields.Integer(allow_none=False)
    updated = fields.Integer()
    initialized = fields.Boolean()

    @post_load
    def make_subreddit(self, data, **kwargs):
        return Subreddit(**data)
