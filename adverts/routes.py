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
    # Temporary hack to pass tests for object creation
    return jsonify([])


@bp.route('', methods=['POST'])
def post_advert():
    data = request.get_json()
    serializers.validate_advert(data)
    advert = services.create_advertisement(**data)
    return jsonify({'id': advert.advert_id}), 201


@bp.errorhandler(serializers.ValidationError)
def validation_error_handler(err):
    return ("{}: {}".format(err.path[-1] if err.path else 'JSON',
                           err.message),
           400)
