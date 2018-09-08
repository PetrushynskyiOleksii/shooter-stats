"""Collection of game statistic endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app.models import Player
from app.schemes import player_schema

from . import shooter_api


@shooter_api.route('/players/<string:nickname>', methods=['GET'])
def get_player(nickname):
    """Retrieve single player instance from database."""
    player = Player.get_by_nickname(nickname)
    if player is None:
        return jsonify({'message': 'Player instance could not be found.'}), 404

    response = player.to_dict(player_schema)
    return jsonify(response.data), 200


@shooter_api.route('/players', methods=['POST'])
def create_player():
    """Create new player instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = Player.from_dict(json_data, player_schema)
    except ValidationError as err:
        return jsonify(err.messages), 400

    player = Player.get_by_nickname(data.get('nickname'))
    if player:
        return jsonify({'error': 'Player with this nickname already exists.'}), 400

    # Create a new player instance
    player = Player(data)

    response = player.to_dict(player_schema)
    return jsonify(response.data), 201


@shooter_api.route('/servers/<string:endpoint>/top_players', methods=['GET'])
def get_top_server_players(endpoint):
    """Return list of top killers/suiciders/assisters on server."""
    # TODO: check for exist endpoint
    order_by = request.args.get('order_by', 'kills')
    limit = int(request.args.get('limit', 25))
    players = Player.get_top_server_players(endpoint, order_by=order_by, limit=limit)

    response = player_schema.dump(players, many=True)
    return jsonify(response.data), 200
