from marshmallow import Schema, fields, post_load
from booru.models.histogram import Histogram


class HistogramSchema(Schema):
    """
    A Schema representing a Histogram in the LZBooru database.
    """
    
    id = fields.Integer()
    red = fields.List(fields.Integer(), allow_none=False)
    green = fields.List(fields.Integer(), allow_none=False)
    blue = fields.List(fields.Integer(), allow_none=False)

    @post_load
    def make_histogram(self, data, **kwargs):
        return Histogram(**data)
