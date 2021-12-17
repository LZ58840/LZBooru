from booru.database import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(), unique=True, nullable=False)
    