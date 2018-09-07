"""Collection of game statistic endpoints."""

from flask import jsonify

from app import db
from app.models.players import Player
from app.models.schemes import player_schema
from . import players_api


@players_api.route('/<string:nickname>', methods=['GET'])
def get_player(nickname):
    """Retrieve single player instance from database."""
    player = db.session.query(Player).filter(Player.nickname == nickname).one()
    if player is None:  # TODO: 404_response()
        return jsonify({'message': 'Player instance could not be found.'}), 404

    print(player)
    response = player_schema.dump(player)
    return jsonify(response.data), 200
