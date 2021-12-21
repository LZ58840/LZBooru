from booru.database import db


class Submission(db.Model):
    url = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    contributor = db.Column(db.String(20), db.ForeignKey('contributor.name'), nullable=False)
    subreddit = db.Column(db.String(20), db.ForeignKey('subreddit.name'), nullable=False)
    created = db.Column(db.Integer, nullable=False)
    flair = db.Column(db.String(64), nullable=False)
    image = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    nsfw = db.Column(db.Boolean, nullable=False, default=False)
    removed = db.Column(db.Boolean, nullable=False, default=False)
