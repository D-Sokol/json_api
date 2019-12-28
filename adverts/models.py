from . import db


class Advertisement(db.Model):
    __tablename__ = 'advertisements'

    advert_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    @property
    def main_photo(self):
        return Photo.query.filter(Photo.advert_id == self.advert_id).order_by(Photo.photo_id.asc()).first()


class Photo(db.Model):
    __tablename__ = 'photos'

    photo_id = db.Column(db.Integer, primary_key=True)
    advert_id = db.Column(db.Integer, db.ForeignKey('advertisements.advert_id'), nullable=False)
    photo_link = db.Column(db.String(150), nullable=False)

    advert = db.relationship('Advertisement', backref='all_photos')
