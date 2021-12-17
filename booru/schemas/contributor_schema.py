from marshmallow import Schema, fields, post_load
from booru.models.contributor import Contributor


class ContributorSchema(Schema):
    id = fields.Integer()
    name = fields.String(allow_none=False)

    @post_load
    def make_contributor(self, data, **kwargs):
        return Contributor(**data)
