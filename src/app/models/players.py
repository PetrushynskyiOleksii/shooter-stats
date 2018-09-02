"""Players models for database representations."""

from app import db


class Player(db.Model):
    """Player database representation."""

    # TODO: abstract class

    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False, unique=True)
    kills = db.Column(db.Integer, nullable=False, default=0)
    deaths = db.Column(db.Integer, nullable=False, default=0)
    assists = db.Column(db.Integer, nullable=False, default=0)
    matches = db.relationship('MatchPlayer', backref='player', lazy=True)

    def __init__(self, data):
        """Player model constructor."""
        self.nickname = data.get('nickname')
        self.kills = data.get('kills', 0)
        self.deaths = data.get('deaths', 0)
        self.assists = data.get('assists', 0)

    def __repr__(self):
        """Return player instance as a string."""
        return f'{self.nickname}'

    @property
    def kda(self):
        """Return KDA value."""
        # TODO
        pass


class MatchPlayer(db.Model):
    """Match player database representation."""

    # TODO: abstract class

    __tablename__ = 'match_player'

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          nullable=False, primary_key=True)
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        """Match player model constructor."""
        self.kills = data.get('kills')
        self.deaths = data.get('deaths')
        self.assists = data.get('assists')
