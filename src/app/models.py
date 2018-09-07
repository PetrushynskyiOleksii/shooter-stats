"""Collections of database models."""

from . import db


class BaseManager(object):
    """Base query manager."""

    def _save(self):
        """Save instance in database."""
        db.session.add(self)
        db.session.commit()


class Server(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'servers'

    endpoint = db.Column(db.String(64), nullable=False, primary_key=True)
    title = db.Column(db.String(64), nullable=False)

    def __init__(self, data):
        """Server model constructor."""
        self.endpoint = data.get('endpoint')
        self.title = data.get('title')

        self._save()

    def __repr__(self):
        """Return server instance as a string."""
        return f'{self.title} ({self.id})'

    @classmethod
    def get_by_endpoint(cls, endpoint):
        """Retrieve single server instance."""
        server = db.session.query(cls).filter(cls.endpoint == endpoint).first()
        return server


class Player(db.Model, BaseManager):
    """Player database representation."""

    __tablename__ = 'players'

    nickname = db.Column(db.String(128), nullable=False, primary_key=True)
    kills = db.Column(db.Integer, nullable=False, default=0)
    deaths = db.Column(db.Integer, nullable=False, default=0)
    assists = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, data):
        """Player model constructor."""
        self.nickname = data.get('nickname')

        self._save()

    def __repr__(self):
        """Return player instance as a string."""
        return f'{self.nickname}'


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
