from marshmallow import Schema, fields, post_load
from booru.models.dhash import Dhash


class DhashSchema(Schema):
    """
    A Schema representing a Dhash in the LZBooru database.
    """
    
    id = fields.Integer()
    red = fields.String(allow_none=False)
    green = fields.String(allow_none=False)
    blue = fields.String(allow_none=False)

    @post_load
    def make_dhash(self, data, **kwargs):
        return Dhash(**data)
