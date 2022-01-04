from booru.database import db


class Link(db.Model):
    id = db.Column(db.String(10), db.ForeignKey('submission.id'), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    created = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String())
    last_visited = db.Column(db.Integer)
    priority = db.Column(db.Integer, nullable=False, default=0)
