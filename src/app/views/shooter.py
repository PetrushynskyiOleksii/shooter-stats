"""Collection of game statistic endpoints."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app import db
from app.models.shooter import Server, Match
from app.models.schemes import (
    server_schema, servers_schema,
    matches_schema, match_schema
)

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
            return jsonify({'error': 'Server with this endpoint already exists.'}), 400

        # Create a new server instance
        server = Server(data)
        server.save()

        response = server_schema.dump(server).data
        status_code = 201

    return jsonify(response), status_code


@shooter_api.route('/<string:endpoint>', methods=['GET', 'PATCH'])
def get_or_update_server(endpoint):
    """Return single server instance with endpoint=`endpoint`."""
    server = Server.query.filter_by(endpoint=endpoint).first()  # TODO: get or 404
    if server is None:
        return jsonify({'message': 'Server instance could not be found.'}), 404

    if request.method == 'PATCH':
        # Update server instance
        json_data = request.get_json()
        server.title = json_data.get('title', server.title)
        db.session.commit()

    response = server_schema.dump(server).data
    return jsonify(response), 200


@shooter_api.route('/<string:endpoint>/matches', methods=['GET', 'POST'])
def create_or_list_matches(endpoint):
    """Create new match instance or return matches list."""
    if request.method == 'GET':
        # Query all existing matches for specify server
        matches = db.session.query(Match).join(Server).filter(
            Server.endpoint == endpoint
        ).all()
        # Serialize the queryset
        response = matches_schema.dump(matches).data
        status_code = 200

    else:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided.'}), 400
        # Validate and deserialize input
        try:
            data = match_schema.load(json_data).data
        except ValidationError as err:
            return jsonify(err.messages), 400

        data['server_endpoint'] = endpoint
        match = Match(data)
        match.save()

        response = match_schema.dump(match).data
        status_code = 201

    return jsonify(response), status_code


@shooter_api.route('/<string:endpoint>/matches/<int:id>', methods=['GET'])
def get_match(endpoint, id):  # FIXME: endpoint arg
    """Return single match instance in JSON representation."""
    match = Match.query.get(id)  # TODO: get or 404
    if match is None:
        return jsonify({'message': 'Match instance could not be found.'}), 404

    response = match_schema.dump(match).data
    return jsonify(response), 200
