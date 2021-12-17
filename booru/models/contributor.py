from booru.database import db


class Contributor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    submissions = db.relationship('Submission', backref='submission_contributor', lazy=True)
