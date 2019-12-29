from . import db
from .models import Advertisement, Photo


def get_advertisement(advert_id):
    return Advertisement.query.get_or_404(advert_id)


def get_advertisements_list(page, order=None, desc=False, page_size=10):
    query = Advertisement.query
    if order is not None:
        field = Advertisement.price if order == 'price' else Advertisement.advert_id
        field = fields.desc() if desc else field.asc()
        query = query.order_by(field)
    if page is not None:
        page += 1
        query = query.offset(page * page_size).limit(page_size)
    return query.all()


def create_advertisement(title, description, price, photo_links):
    advert = Advertisement(title=title, description=description, price=price)
    db.session.add(advert)
    for link in photo_links:
        advert.all_photos.append(Photo(photo_link=link))
    db.session.commit()
    return advert
