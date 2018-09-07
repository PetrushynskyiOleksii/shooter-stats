"""Collection of game statistic endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app.models import Match, Player
from app.schemes import player_schema, matches_schema

from . import shooter_api


@shooter_api.route('/players/<string:nickname>', methods=['GET'])
def get_player(nickname):
    """Retrieve single player instance from database."""
    player = Player.get_by_nickname(nickname)
    if player is None:
        return jsonify({'message': 'Player instance could not be found.'}), 404

    response = player_schema.dump(player)
    return jsonify(response.data), 200


@shooter_api.route('/players/<string:nickname>/matches', methods=['GET'])
def get_player_matches(nickname):
    """Retrieve player matches from database."""
    matches = Match.get_matches(nickname)
    # TODO: paginate response
    response = matches_schema.dump(matches)
    return jsonify(response.data), 200


@shooter_api.route('/players', methods=['POST'])
def create_player():
    """Create new player instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = player_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 400

    player = Player.get_by_nickname(data.get('nickname'))
    if player:
        return jsonify({'error': 'Player with this nickname already exists.'}), 400

    # Create a new player instance
    player = Player(data)

    response = player_schema.dump(player)
    return jsonify(response.data), 201
