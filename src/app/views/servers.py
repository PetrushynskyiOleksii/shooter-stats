"""Handlers collection of server model endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app.models import Server
from app.schemes import server_schema
from . import shooter_api


@shooter_api.route('/servers', methods=['GET'])
def get_servers():
    """Retrieve all existing servers from database."""
    servers = Server.get_all()

    response = servers.to_dict(servers, many=True)
    return jsonify(response.data), 200


@shooter_api.route('/servers', methods=['POST'])
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

    server = Server.get_by_endpoint(data.get('endpoint'))
    if server:
        return jsonify({'error': 'Server with this endpoint already exists.'}), 400

    # Create a new server instance
    server = Server(data)

    response = server.to_dict()
    return jsonify(response.data), 201


@shooter_api.route('/servers/<string:endpoint>', methods=['GET', 'PATCH'])
def get_or_update_server(endpoint):
    """Retrieve or update single server instance in database."""
    server = Server.get_by_endpoint(endpoint)
    if server is None:
        return jsonify({'message': 'Server instance could not be found.'}), 404

    if request.method == 'PATCH':
        # Update server instance
        json_data = request.get_json()
        server.update(json_data.get('title'))

    response = server.to_dict()
    return jsonify(response.data), 200
