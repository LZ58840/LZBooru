from booru.database import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(), nullable=False)
    submission_id = db.Column(db.String(10), db.ForeignKey('submission.id'), nullable=False)
    