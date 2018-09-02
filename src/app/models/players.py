"""Players models for database representations."""

from app import db


class MatchPlayer(db.Model):
    """Match player database representation."""

    # TODO: abstract class

    __tablename__ = 'match_players'

    id = db.Column(db.Integer, primary_key=True)
    # TODO: player (foreign key - player)
    kills = db.Column(db.Integer)
    deaths = db.Integer(db.Integer)
    assists = db.Integer(db.Integer)

    def __init__(self, data):
        """Match player model constructor."""
        self.kills = data.get('kills')
        self.deaths = data.get('deaths')
        self.assists = data.get('assists')

    @property
    def kda(self):
        """Return KDA value."""
        # TODO
        pass
