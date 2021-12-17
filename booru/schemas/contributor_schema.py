from marshmallow import Schema, fields, post_load
from booru.models.contributor import Contributor


class ContributorSchema(Schema):
    name = fields.String()

    @post_load
    def make_contributor(self, data, **kwargs):
        return Contributor(**data)
