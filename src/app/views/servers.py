"""Handlers collection of server model endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.models.shooter import Server, Match
from app.models.players import Player
from app.models.schemes import servers_schema, server_schema, players_schema
from . import shooter_api


@shooter_api.route('/', methods=['GET'])
def get_servers():
    """Retrieve all existing servers from database."""
    servers = db.session.query(Server).all()
    response = servers_schema.dump(servers)

    return jsonify(response.data), 200


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

    server = db.session.query.filter(Server.endpoint == data.get('endpoint')).first()
    if server:
        return jsonify({'error': 'Server with this endpoint already exists.'}), 400

    # Create a new server instance
    server = Server(data)
    db.session.add(server)
    db.session.commit()

    response = server_schema.dump(server)

    return jsonify(response.data), 201


@shooter_api.route('/<string:endpoint>', methods=['GET', 'PATCH'])
def get_or_update_server(endpoint):
    """Retrieve or update single server instance in database."""
    server = db.session.query.filter(Server.endpoint == endpoint).first()  # TODO: get or 404
    if server is None:
        return jsonify({'message': 'Server instance could not be found.'}), 404

    if request.method == 'PATCH':
        # Update server instance
        json_data = request.get_json()
        server.title = json_data.get('title', server.title)
        db.session.commit()

    response = server_schema.dump(server)
    return jsonify(response.data), 200


@shooter_api.route('/<string:endpoint>/players', methods=['GET'])
def get_top_server_killers(endpoint):
    """Return list of top killers on server."""
    players = db.session.query(Player).join(Player.matches).filter(
        Match.server_endpoint == endpoint
    ).order_by(Player.kills.desc()).all()[:25]

    response = players_schema.dump(players)
    return jsonify(response.data), 200
