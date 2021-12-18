from marshmallow import Schema, fields, post_load
from booru.models.subreddit import Subreddit


class SubredditSchema(Schema):
    name = fields.String()
    created = fields.DateTime(allow_none=False)
    updated = fields.DateTime()
    initialized = fields.Boolean()

    @post_load
    def make_subreddit(self, data, **kwargs):
        return Subreddit(**data)
