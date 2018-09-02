"""Players models for database representations."""

from app import db


class MatchPlayer(db.Model):
    """Match player database representation."""

    # TODO: abstract class

    __tablename__ = 'match_players'

    id = db.Column(db.Integer, primary_key=True)
    # TODO: player (foreign key - player)
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Integer(db.Integer, nullable=False)
    assists = db.Integer(db.Integer, nullable=False)

    def __init__(self, data):
        """Match player model constructor."""
        self.kills = data.get('kills')
        self.deaths = data.get('deaths')
        self.assists = data.get('assists')


class Player(db.Model):
    """Player database representation."""

    # TODO: abstract class

    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False)
    kills = db.Column(db.Integer, nullable=False, default=0)
    deaths = db.Integer(db.Integer, nullable=False, default=0)
    assists = db.Integer(db.Integer, nullable=False, default=0)

    def __init__(self, data):
        """Player model constructor."""
        self.nickname = data.get('nickname', 0)
        self.kills = data.get('kills', 0)
        self.deaths = data.get('deaths', 0)
        self.assists = data.get('assists', 0)

    @property
    def kda(self):
        """Return KDA value."""
        # TODO
        pass
