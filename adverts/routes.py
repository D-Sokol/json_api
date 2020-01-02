from flask import Blueprint, request, jsonify

from . import services
from . import serializers

bp = Blueprint('advertisements', __name__, url_prefix='/advertisement')

@bp.route('/<int:advert_id>', methods=['GET'])
def get_advert_item(advert_id):
    return jsonify(serializers.advert_to_json(
        services.get_advertisement(advert_id),
        request.args.get('fields', '')
    ))


@bp.route('', methods=['GET'])
def get_advert_collection():
    return 'ok'


@bp.route('', methods=['POST'])
def post_advert():
    return 'ok'
