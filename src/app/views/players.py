"""Collection of game statistic endpoints."""

from flask import jsonify, request

from app.models.players import Player
from app.models.schemes import players_schema
from . import players_api


@players_api.route('/', methods=['GET'])
def get_players():
    """Return list of all existing player."""
    if request.method == 'GET':
        # Query all existing players
        players = Player.query.all()
        # Serialize the queryset
        response = players_schema.dump(players).data

    return jsonify(response), 200
