from booru.database import db


class Subreddit(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    created = db.Column(db.Integer, nullable=False)
    updated = db.Column(db.Integer)
    initialized = db.Column(db.Boolean, nullable=False, default=False)
    submissions = db.relationship('Submission', backref='submission_subreddit', lazy=True)
