from flask import request, jsonify

from . import app
from . import services
from . import serializers

@app.route('/advertisement/<int:advert_id>', methods=['GET'])
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
    """
    return jsonify(serializers.advert_to_json(
        services.get_advertisement(advert_id),
        request.args.get('fields', '')
    ))


@app.route('/advertisement', methods=['GET'])
def get_advert_collection():
    return 'ok'


@app.route('/advertisement', methods=['POST'])
def post_advert():
    return 'ok'
