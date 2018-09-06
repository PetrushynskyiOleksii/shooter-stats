"""Players models for database representations."""

from . import db


class Player(db.Model):
    """Player database representation."""

    __tablename__ = 'players'

    nickname = db.Column(db.String(128), nullable=False, primary_key=True)
    kills = db.Column(db.Integer, nullable=False, default=0)
    deaths = db.Column(db.Integer, nullable=False, default=0)
    assists = db.Column(db.Integer, nullable=False, default=0)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=True)

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
