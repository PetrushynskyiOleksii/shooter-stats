"""Stats models for database representation."""

from . import db, BaseManager


class Server(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'servers'

    endpoint = db.Column(db.String(64), nullable=False, primary_key=True)
    title = db.Column(db.String(64), nullable=False)

    def __init__(self, data):
        """Post model constructor."""
        self.endpoint = data.get('endpoint')
        self.title = data.get('title')

    def __repr__(self):
        """Return server instance as a string."""
        return f'{self.title} ({self.id})'


scoreboards = db.Table(
    'scoreboards',
    db.Column('match_id', db.Integer, db.ForeignKey('matches.id'), primary_key=True),
    db.Column('player_nickname', db.String(128),
              db.ForeignKey('players.nickname'), primary_key=True
              )
)


class Match(db.Model, BaseManager):
    """Match database representation."""

    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(48), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    server_endpoint = db.Column(db.String(64), db.ForeignKey('servers.endpoint'))
    server = db.relationship('Server', backref=db.backref('matches', lazy='subquery'))
    scoreboard = db.relationship('Player', secondary=scoreboards, lazy='subquery',
                                 backref=db.backref('matches', lazy=True))

    def __init__(self, data):
        """Match model constructor."""
        self.title = data.get('title')
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')
        self.server_endpoint = data.get('server_endpoint')

    def __repr__(self):
        """Return match instance as a string."""
        return f'{self.title}'
