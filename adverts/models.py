from . import db


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    advert_id = db.Column(db.Integer, primary_key=True)
