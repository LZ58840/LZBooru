from marshmallow import Schema, fields, post_load
from booru.models.image import Image


class ImageSchema(Schema):
    """
    A Schema representing an Image in the LZBooru database.
    """

    id = fields.Integer()
    url = fields.String(allow_none=False)
    submission_id = fields.String(allow_none=False)

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)