from jsonschema import validate

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
