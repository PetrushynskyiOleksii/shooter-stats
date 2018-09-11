"""Collection of game statistic endpoints."""

from flask import jsonify, request

from app import db
from app.models import Match, Player, Scoreboard
from app.utils import paginate_response


def get_match(endpoint, id):  # FIXME: endpoint arg
    """Return single match instance in JSON representation."""
    match = Match.get(id)
    if match is None:
        return jsonify({'message': 'Match instance could not be found.'}), 404

    response = match.to_dict()
    return jsonify(response), 200


def create_match(endpoint):
    """Create a new match instance."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No required input data provided.'}), 400

    # TODO: check for exist endpoint
    data, errors = Match.from_dict(json_data)
    if errors:
        return jsonify(errors), 400

    # Create new match
    data['server'] = endpoint
    match = Match(data)
    match.save()

    # Update players data
    for player in data.get('players'):
        match_player = Scoreboard(player_data=player, match_id=match.id)
        player_for_upd = db.session.query(Player).filter(
            Player.nickname == player.get('nickname')
        ).with_for_update().one()
        player_for_upd.kills += player.get('kills')
        player_for_upd.deaths += player.get('deaths')
        player_for_upd.assists += player.get('assists')

        match.players.append(match_player)

    db.session.commit()
    response = match.to_dict()

    return jsonify(response), 201


def get_player_matches(nickname):
    """Retrieve player matches from database."""
    page = request.args.get('page', 1, type=int)
    matches = Match.get_player_matches(nickname)

    response = paginate_response(matches, page)
    return jsonify(response), 200


def get_server_matches(endpoint):
    """Return all existing matches for a specify server."""
    page = request.args.get('page', 1, type=int)
    matches = Match.get_server_matches(endpoint)

    response = paginate_response(matches, page)
    return jsonify(response), 200
