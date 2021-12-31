from marshmallow import Schema, fields, post_load
from booru.models.link import Link


class LinkSchema(Schema):
    id = fields.String()
    url = fields.String(allow_none=False)
    created = fields.Integer(allow_none=False)

    @post_load
    def make_link(self, data, **kwargs):
        return Link(**data)