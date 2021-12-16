from booru.database import db


class Submission(db.Model):
    link_id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    flair = db.Column(db.String(64), nullable=False)
    img = db.Column(db.String(), nullable=False)
    removed = db.Column(db.Boolean, nullable=False, default=False)
