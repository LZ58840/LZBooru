from booru.database import db


class Contributor(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    submissions = db.relationship('Submission', backref='submission_contributor', lazy=True)
