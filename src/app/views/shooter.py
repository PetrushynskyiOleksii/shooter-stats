"""Collection of game statistic endpoints."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.models.schemes import server_schema
from app.models.shooter import Server

shooter_api = Blueprint('shooter', __name__)


@shooter_api.route('/', methods=['POST'])
def create_server():
    """Create new server instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = server_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 400

    server = Server.query.filter_by(endpoint=data.get('endpoint')).first()
    if server:
        return jsonify({'error': 'This endpoint already exists.'}), 400

    # Create a new server instance
    server = Server(data)
    server.save()
    response = server_schema.dump(server).data

    return jsonify(response), 201
