"""Collection of game statistic endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.models import Match, Player
from app.schemes import match_schema
from . import shooter_api


@shooter_api.route('/servers/<string:endpoint>/matches', methods=['GET'])
def get_matches(endpoint):
    """Return all existing matches for a specify server."""
    matches = Match.get_server_matches(endpoint)

    response = match_schema.dump(matches, many=True)
    return jsonify(response.data), 200


@shooter_api.route('/servers/<string:endpoint>/matches/<int:id>', methods=['GET'])
def get_match(endpoint, id):  # FIXME: endpoint arg
    """Return single match instance in JSON representation."""
    match = Match.get(id)  # TODO: get or 404
    if match is None:
        return jsonify({'message': 'Match instance could not be found.'}), 404

    response = match.to_dict()
    return jsonify(response), 200


@shooter_api.route('/servers/<string:endpoint>/matches', methods=['POST'])
def create_match(endpoint):
    """Create a new match instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided.'}), 400

    # TODO: check for exist endpoint
    # Validate and deserialize  input
    try:
        data = match_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Create new match
    data['server'] = endpoint
    match = Match(data)

    # Update players data
    for player in data.get('scoreboard'):
        player_for_upd = db.session.query(Player).filter(
            Player.nickname == player.get('nickname')
        ).with_for_update().one()
        player_for_upd.kills += player.get('kills')
        player_for_upd.deaths += player.get('deaths')
        player_for_upd.assists += player.get('assists')

        match.scoreboard.append(player_for_upd)

    match.save()
    response = match.to_dict()

    return jsonify(response.data), 201


@shooter_api.route('/players/<string:nickname>/matches', methods=['GET'])
def get_player_matches(nickname):
    """Retrieve player matches from database."""
    matches = Match.get_matches(nickname)
    # TODO: paginate response
    response = match_schema.dump(matches, many=True)
    return jsonify(response.data), 200
