from booru.database import db


class Subreddit(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    submissions = db.relationship('Submission', backref='submission_subreddit', lazy=True)
