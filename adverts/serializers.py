from jsonschema import validate, ValidationError

advertisement_model = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string", "maxLength": 200},
        "description": {"type": "string", "maxLength": 1000},
        "price": {"type": "number", "minimum": 0.0},
        "photo_links": {
            "type": "array",
            "maxItems": 3,
            "items": {"type": "string", "maxLength": 150}
        }
    },
    "required": ["title", "description", "price"]
}


def validate_advert(json):
    """
    Проверяет, соответствует ли переданный словарь требованиям к модели для создания объявления.
    Если словарь json не может быть использован для создания объекта объявления,
    выбрасывается исключение типа jsonschema.ValidationError, в противном случае функция возвращает None.
    :param dict json:
    :return None:
    """
    validate(json, advertisement_model)


def photo_to_json(photo):
    """
    Выполняет сериализацию объекта типа adverts.models.Photo в тип, поддерживаемый JSON.
    Возвращает строку, представляющую ссылку на фотографию.
    Если ссылка отсутствует или в качестве аргумента передано None, возвращает None
    :param Photo photo:
    :return str:
    """
    return photo.photo_link if photo is not None else None


def advert_to_json(advert, fields=''):
    """
    Выполняет сериализацию объекта типа adverts.models.Advertisement в JSON.
    Возвращает словарь, содержащий название объявления, цену и ссылку на главное фото.
    Также в результат могут быть включено описание и массив ссылок на все фотографии.
    Для этого необходимо в качестве параметра fields передать строку, содержащую
     названия дополнительных полей, разделенные запятой.
    :param Advertisement advert:
    :param str fields:
    :return dict:
    """
    fields = fields.split(',')
    json = {
        'title': advert.title,
        'price': advert.price,
        'main_photo': photo_to_json(advert.main_photo),
    }
    if 'description' in fields:
        json['description'] = advert.description
    if 'all_photos' in fields:
        json['all_photos'] = list(map(photo_to_json, advert.all_photos))
    return json
