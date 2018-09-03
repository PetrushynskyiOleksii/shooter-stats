"""Collection of game statistic endpoints."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.models.schemes import server_schema, servers_schema
from app.models.shooter import Server
from app import db

shooter_api = Blueprint('shooter', __name__)


@shooter_api.route('/', methods=['POST', 'GET'])
def create_or_list_servers():
    """Create new server instance or return servers list."""
    if request.method == 'GET':
        # Query all existing servers
        servers = Server.query.all()
        # Serialize the queryset
        response = servers_schema.dump(servers).data
        status_code = 200

    else:
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
        status_code = 201

    return jsonify(response), status_code


@shooter_api.route('/<string:endpoint>', methods=['GET', 'PATCH'])
def get_or_update_server(endpoint):
    """Return single server instance with endpoint=`endpoint`."""
    server = Server.query.filter_by(endpoint=endpoint).first()
    if server is None:
        return jsonify({'message': 'Server instance could not be found.'}), 400

    if request.method == 'PATCH':
        # Update server instance
        json_data = request.get_json()
        server.title = json_data.get('title', server.title)
        db.session.commit()

    response = server_schema.dump(server).data
    return jsonify(response), 200
