from booru.database import db


class Submission(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    subreddit = db.Column(db.String(20), db.ForeignKey('subreddit.name'), nullable=False)
    created = db.Column(db.Integer, nullable=False)
    flair = db.Column(db.String(64), nullable=True)
    images = db.relationship('Image', backref="submission_image", lazy=True)
    link = db.relationship('Link', backref="submission_link", lazy=True)
    nsfw = db.Column(db.Boolean, nullable=False, default=False)
    removed = db.Column(db.Boolean, nullable=False, default=False)
