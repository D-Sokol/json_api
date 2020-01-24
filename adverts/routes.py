from flask import Blueprint, request, jsonify

from . import services
from . import serializers

bp = Blueprint('advertisements', __name__, url_prefix='/advertisement')

@bp.route('/<int:advert_id>', methods=['GET'])
def get_advert_item(advert_id):
    """
    Возвращает в формате JSON одно ранее созданное объявление, соответствующее переданному ID.
    Если запрошенного объявления не существует, возвращает HTTP код 404.
    Набор полей, добавляемых в ответ, зависит от GET-аргумента fields.
    Ожидается, что в качестве fields передается набор имен полей, который необходимо включить в ответ,
     разделенный запятой.

    JSON-представление объявления содержит следующие поля:
    title (string) -- название объявления.
    price (number) -- цена, указанная при создании объявления.
    main_photo (string или null) -- ссылка на первую фотографию, прикрепленную к объявлению.
    description (string) -- описание объявления. Возвращается, только если указано в параметре fields.
    all_photos (array of string) -- набор ссылок на фотографии, прикрепленные к объявлению.
                                    Возвращается, только если указано в параметре fields.

    Пример тела ответа сервера в случае, когда оба дополнительных поля указаны в параметре fields
     (то есть, fields="description,all_photos"):
    {"title": "Snake", "price": 495.0, "main_photo": "http://example.com/images/11.png", "description": "Sell a snake", "all_photos": ["http://example.com/images/11.png", "http://example.com/images/12.png"]}
    """
    return jsonify(serializers.advert_to_json(
        services.get_advertisement(advert_id),
        request.args.get('fields', '')
    ))


@bp.route('', methods=['GET'])
def get_advert_collection():
    """
    Возвращает в формате JSON массив объявлений, расположенных на выбранной странице с учетом сортировки.
    Если ни одно объявление не оказывается на выбранной странице, возвращается HTTP код 200 и пустой массив.
    Модель, используемая для сериализации объявлений, совпадает с моделью, используемой в API '/advertisement/<id>'
     с пустым параметром fields.

    Размещение объявлений на страницах управляется следующими GET-аргументами:
    sort -- принимаются значения 'price', 'date'. Задает критерий, по которому упорядочиваются объявления.
    order -- принимаются значения 'asc', 'desc'. Задает порядок сортировки: по возрастанию или по убыванию.
    page -- номер страницы, целое положительное число. Обязательный аргумент.

    При разбиении на страницы размер страницы принимается равным 10. Это число не регулируется параметрами запроса.
    """
    order = request.args.get('sort')
    desc = (request.args.get('order') == 'desc')
    page = int(request.args.get('page', 1))
    if page <= 0:
        raise ValueError("Page number must be positive, got {}".format(page))
    adverts = services.get_advertisements_list(page, order, desc)
    return jsonify([
        serializers.advert_to_json(advert)
        for advert in adverts
    ])


@bp.route('', methods=['POST'])
def post_advert():
    """
    Принимает в теле запроса JSON-модель объявления и сохраняет новый объект объявления в базу данных.
    В случае успешного создания объекта возвращает идентификатор объявления и HTTP статус 201.
    Если переданная модель не удовлетворяет предъявляемым требованиям, возвращает HTTP статус 400 и строку с причиной ошибки.

    Пример тела ответа сервера в случае успешного создания объявления:
    {"id": 42}

    Пример тела запроса, удовлетворяющего всем ограничениям:
    {"title": "Unicorn", "description": "Sell an unicorn.", "price": 42, "photo_links": ["http://example.com/images/1.png", "http://example.com/images/2.png", "http://example.com/images/3.png"]}

    Пример тела ответа сервера в случае, когда модель в теле запроса не проходит валидацию:
    "price: -50.0 is less than the minimum of 0.0"
    """
    data = request.get_json()
    serializers.validate_advert(data)
    advert = services.create_advertisement(**data)
    return jsonify({'id': advert.advert_id}), 201


@bp.errorhandler(ValueError)
def bad_page_number_handler(err):
    return str(err), 400

@bp.errorhandler(serializers.ValidationError)
def validation_error_handler(err):
    return ("{}: {}".format(err.path[-1] if err.path else 'JSON',
                           err.message),
           400)
