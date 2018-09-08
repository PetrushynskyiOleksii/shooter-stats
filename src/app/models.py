"""Collections of database models."""

from . import db
from .schemes import match_schema


class BaseManager(object):
    """Base query manager."""

    def _save(self):
        """Save instance in database."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def from_dict(json_data, schema):
        """Return instance as python's data types."""
        schema_response = schema.load(json_data)
        return schema_response

    def to_dict(self, schema):
        """Return instance as JSON dict."""
        data = schema.dump(self)
        return data


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
        """Retrieve single server instance from database."""
        server = db.session.query(cls).filter(cls.endpoint == endpoint).first()
        return server

    @classmethod
    def get_all(cls, order_by):
        """Retrieve all existing servers from database."""
        query = db.session.query(cls)
        if order_by == 'title':
            servers = query.order_by(cls.title).all()
        elif order_by == 'endpoint':
            servers = query.order_by(cls.endpoint).all()
        else:
            servers = query.all()

        return servers

    def update(self, new_title):
        """Update title of server."""
        if self.title != new_title:
            self.title = new_title
            db.session.commit()

        return self.title


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

    @classmethod
    def get_by_nickname(cls, nickname):
        """Retrieve single player instance from database."""
        player = db.session.query(cls).filter(cls.nickname == nickname).first()
        return player

    @classmethod
    def get_top_server_players(cls, endpoint, order_by, limit):
        """Retrieve limited list of top players by kills/deaths/assists."""
        top_players = db.session.query(cls).join(cls.matches).filter(
            Match.server_endpoint == endpoint
        )

        if order_by == 'kills':
            top_players = top_players.order_by(Player.kills.desc())
        elif order_by == 'deaths':
            top_players = top_players.order_by(Player.deaths.desc())
        elif order_by == 'assists':
            top_players = top_players.order_by(Player.assists.desc())

        return top_players.all()[:limit]


scoreboards = db.Table(
    'scoreboards',
    db.Column('match_id', db.Integer, db.ForeignKey('matches.id'), primary_key=True),
    db.Column('player_nickname', db.String(128),
              db.ForeignKey('players.nickname'), primary_key=True
              )
)


class Match(db.Model):
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
        self.server_endpoint = data.get('server')

    def __repr__(self):
        """Return match instance as a string."""
        return f'{self.title}'

    def save(self):
        """Save match instance to database."""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_player_matches(cls, nickname):
        """Retrieve player matches from database."""
        query = db.session.query(cls).join(cls.scoreboard).filter(Player.nickname == nickname)
        matches = query.order_by(cls.end_time.desc()).all()
        return matches

    @classmethod
    def get_server_matches(cls, endpoint):
        """Retrieve server matches ordered by end_time from database."""
        query = db.session.query(cls).join(Server).filter(Server.endpoint == endpoint)
        matches = query.order_by(cls.end_time.desc()).all()
        return matches

    @classmethod
    def get(cls, id):
        """Retrieve single match instance from database."""
        match = db.session.query(cls).filter(cls.id == id).first()
        return match

    def to_dict(self):
        """Return match instance as JSON dict."""
        data = match_schema.dump(self)
        return data

    @staticmethod
    def from_dict(json_data):
        """Return match instance as python's data types."""
        schema_response = match_schema.load(json_data)
        return schema_response