"""Collection of game statistic endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.models.shooter import Server, Match
from app.models.schemes import matches_schema, match_schema
from . import shooter_api


@shooter_api.route('/<string:endpoint>/matches', methods=['GET'])
def get_matches(endpoint):
    """Return all existing matches for a specify server."""
    matches = db.session.query(Match).join(Server).filter(  # TODO: improve query
        Server.endpoint == endpoint
    ).all()
    response = matches_schema.dump(matches)

    return jsonify(response.data), 200


@shooter_api.route('/<string:endpoint>/matches/<int:id>', methods=['GET'])
def get_match(endpoint, id):  # FIXME: endpoint arg
    """Return single match instance in JSON representation."""
    match = Match.query.get(id)  # TODO: get or 404
    if match is None:
        return jsonify({'message': 'Match instance could not be found.'}), 404

    response = match_schema.dump(match)
    return jsonify(response), 200


@shooter_api.route('/<string:endpoint>/matches/<int:id>', methods=['POST'])
def create_match(endpoint):
    """Create a new match instance."""
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

    response = match_schema.dump(match)

    return jsonify(response.data), 201
