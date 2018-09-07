"""Collection of game statistic endpoints."""

from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.models.shooter import Match
from app.models.players import Player
from app.models.schemes import player_schema, matches_schema

from . import players_api


@players_api.route('/<string:nickname>', methods=['GET'])
def get_player(nickname):
    """Retrieve single player instance from database."""
    player = db.session.query(Player).filter(Player.nickname == nickname).first()
    if player is None:  # TODO: 404_response()
        return jsonify({'message': 'Player instance could not be found.'}), 404

    response = player_schema.dump(player)
    return jsonify(response.data), 200


@players_api.route('/<string:nickname>/matches', methods=['GET'])
def get_player_matches(nickname):
    """Retrieve player matches from database."""
    matches = db.session.query(Match).join(Match.scoreboard).filter(
        Player.nickname == nickname
    ).all()
    # TODO: paginate response
    response = matches_schema.dump(matches)
    return jsonify(response.data), 200


@players_api.route('/', methods=['POST'])
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

    player = db.session.query(Player).filter(Player.nickname == data.get('nickname')).first()
    if player:
        return jsonify({'error': 'Player with this nickname already exists.'}), 400

    # Create a new player instance
    player = Player(data)
    db.session.add(player)
    db.session.commit()

    response = player_schema.dump(player)

    return jsonify(response.data), 201
