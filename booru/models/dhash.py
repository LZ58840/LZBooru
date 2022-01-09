from booru.database import db
from sqlalchemy.dialects.postgresql import BIT


class Dhash(db.Model):
    """
    A model representing a RGB difference hash of an Image in the LZBooru database.
    """

    id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True, nullable=False)
    red = db.Column(BIT(length=64), nullable=False)
    green = db.Column(BIT(length=64), nullable=False)
    blue = db.Column(BIT(length=64), nullable=False)
