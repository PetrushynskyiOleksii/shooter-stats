"""Collection of game statistic endpoints."""

from flask import jsonify, request

from app.models import Player
from app.utils import paginate_response


def get_player(nickname):
    """Retrieve single player instance from database."""
    player = Player.get_player_stats(nickname)
    if player is None:
        return jsonify({'message': 'Player instance could not be found.'}), 404

    response = player.to_dict()
    return jsonify(response), 200


def create_player():
    """Create new player instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided.'}), 400
    # Validate and deserialize input
    data, errors = Player.from_dict(json_data)
    if errors:
        return jsonify(errors), 400

    player = Player.get(data.get('nickname'))
    if player:
        return jsonify({'error': 'Player with this nickname already exists.'}), 400

    # Create a new player instance
    player = Player(data)

    response = player.to_dict()
    return jsonify(response), 201


def get_server_players(endpoint):
    """Return list of players on server."""
    # TODO: check for exist endpoint
    page = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by')
    players = Player.get_all(order_by=order_by, endpoint=endpoint)

    response = paginate_response(players, page=page)
    return jsonify(response), 200


def get_players():
    """Return all existing players in database."""
    page = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by')
    players = Player.get_all(order_by=order_by)

    response = paginate_response(players, page=page)
    return jsonify(response), 200
