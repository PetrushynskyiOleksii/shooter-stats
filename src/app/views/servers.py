"""Handlers collection of server model endpoints."""

from flask import jsonify, request

from app.models import Server
from app.utils import paginate_response


def get_servers():
    """Retrieve all existing servers from database."""
    page = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by')
    servers = Server.get_all(order_by=order_by)

    response = paginate_response(servers, page)
    return jsonify(response), 200


def create_server():
    """Create new server instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No required input data provided.'}), 400

    data, errors = Server.from_dict(json_data)
    if errors:
        return jsonify(errors), 400

    server = Server.get(data.get('endpoint'))
    if server:
        return jsonify({'error': 'Server with this endpoint already exists.'}), 400

    # Create a new server instance
    server = Server(data)

    response = server.to_dict()
    return jsonify(response), 201


def get_server(endpoint):
    """Retrieve single server instance from database."""
    server = Server.get_server_stats(endpoint)
    if server is None:
        return jsonify({'message': 'Server instance could not be found.'}), 404

    response = server.to_dict()
    return jsonify(response), 200


def update_server(endpoint):
    """Update server instance in database."""
    server = Server.get(endpoint)
    if server is None:
        return jsonify({'message': 'Server instance could not be found.'}), 404

    # Update server instance
    json_data = request.get_json()
    server.update(json_data.get('title'))

    response = server.to_dict()
    return jsonify(response), 200
