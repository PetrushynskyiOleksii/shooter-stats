"""Collection of game statistic endpoints."""

from flask import Blueprint, jsonify, request

from app.models.players import Player
from app.models.schemes import players_schema

players_api = Blueprint('players', __name__)


@players_api.route('/', methods=['GET'])
def get_players():
    """Return list of all existing player."""
    if request.method == 'GET':
        # Query all existing players
        players = Player.query.all()
        # Serialize the queryset
        response = players_schema.dump(players).data

    return jsonify(response), 200
