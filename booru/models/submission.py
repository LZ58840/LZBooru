from booru.database import db


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(10), unique=True, nullable=False)
    title = db.Column(db.String(300), nullable=False)
    contributor = db.Column(db.Integer, db.ForeignKey('contributor.id'), nullable=False)
    subreddit = db.Column(db.Integer, db.ForeignKey('subreddit.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    flair = db.Column(db.String(64), nullable=False)
    image = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    nsfw = db.Column(db.Boolean, nullable=False, default=False)
    removed = db.Column(db.Boolean, nullable=False, default=False)
