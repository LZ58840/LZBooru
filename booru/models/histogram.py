from booru.database import db
from sqlalchemy.dialects.postgresql import ARRAY


class Histogram(db.Model):
    """
    A model representing a RGB Histogram of an Image in the LZBooru database.
    """

    id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True, nullable=False)
    red = db.Column(ARRAY(db.Integer), nullable=False)
    green = db.Column(ARRAY(db.Integer), nullable=False)
    blue = db.Column(ARRAY(db.Integer), nullable=False)
