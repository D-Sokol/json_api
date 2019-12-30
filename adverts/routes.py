from flask import request

from . import app
from . import services


@app.route('/advertisement/<int:advert_id>', methods=['GET'])
def get_advert_item(advert_id):
    return 'ok'


@app.route('/advertisement', methods=['GET'])
def get_advert_collection():
    return 'ok'


@app.route('/advertisement', methods=['POST'])
def post_advert():
    return 'ok'
