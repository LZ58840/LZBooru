from booru.database import db


class Link(db.Model):
    id = db.Column(db.String(10), db.ForeignKey('submission.id'), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    created = created = db.Column(db.Integer, nullable=False)