from . import db
from .models import Advertisement, Photo


def get_advertisement(advert_id):
    """
    Возвращает объект объявления, соответствующий переданному ID, если он существует.
    Если такого объявления нет, выбрасывается исключение типа werkzeug.exceptions.NotFound.
    Этот тип исключения перехватывается веб-сервером, который автоматически возвращает статус 404.
    :param int advert_id:
    :return Advertisement:
    """
    return Advertisement.query.get_or_404(advert_id)


def get_advertisements_list(page, order=None, desc=False, page_size=10):
    """
    Возвращает список, содержащий некоторое подмножество сохраненных в базе данных объявлений.
    Выборка производится следующим образом:
        Если order == 'price', объявления сортируются по цене.
        Если order == 'date', объявления сортируются по дате.
        Если order == None (по умолчанию), порядок объявлений не задается явно.
        В случае, когда порядок задан, объявления располагаются по возрастанию параметра, если desc == False,
         и по убыванию в противном случае.
        После применения сортировки все объявления разбиваются на страницы размера page_size.
        Возвращается список объявлений, для которых номер страницы совпадает с page
    :param int page:
    :param str order:
    :param bool desc:
    :param int page_size:
    :return list:
    """
    query = Advertisement.query
    if order is not None:
        field = Advertisement.price if order == 'price' else Advertisement.advert_id
        field = field.desc() if desc else field.asc()
        query = query.order_by(field)
    if page is not None:
        page -= 1
        query = query.offset(page * page_size).limit(page_size)
    return query.all()


# Since this function usually calls as create_advertisement(**data),
#  and there are no guaranteed that data has key 'photo_links',
#  one should provide reasonable default value.
# Empty tuple is the best choice, because it is iterable, empty and immutable.
def create_advertisement(title, description, price, photo_links=()):
    """
    Создает объект объявления и, при необходимости, объекты фотографий, используя переданные значения полей.
    Также сохраняет все созданные объекты в базу данных.
    Возвращает созданный объект объявления.
    :param str title:
    :param str description:
    :param float price:
    :param list photo_links:
    :return Advertisement:
    """
    advert = Advertisement(title=title, description=description, price=price)
    db.session.add(advert)
    for link in photo_links:
        advert.all_photos.append(Photo(photo_link=link))
    db.session.commit()
    return advert
