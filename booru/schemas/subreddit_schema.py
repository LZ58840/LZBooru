from marshmallow import Schema, fields, post_load
from booru.models.subreddit import Subreddit


class SubredditSchema(Schema):
    name = fields.String()

    @post_load
    def make_subreddit(self, data, **kwargs):
        return Subreddit(**data)
