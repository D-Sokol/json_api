from flask import request, jsonify

from . import app
from . import services
from . import serializers

@app.route('/advertisement/<int:advert_id>', methods=['GET'])
def get_advert_item(advert_id):
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
