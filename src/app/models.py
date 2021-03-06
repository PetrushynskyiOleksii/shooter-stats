"""Collections of database models."""
from sqlalchemy import func, distinct

from . import db
from .schemes import ServerSchema, PlayerSchema, MatchSchema


class SchemaManager(object):
    """Base query manager."""

    @classmethod
    def from_dict(cls, json_data):
        """Return instance as python's data types."""
        schema_response = cls.schema.load(json_data)
        return schema_response

    def to_dict(self):
        """Return instance as JSON dict."""
        schema_response = self.schema.dump(self)
        return schema_response.data


class Server(db.Model, SchemaManager):
    """Server database representation."""

    __tablename__ = 'servers'

    endpoint = db.Column(db.String(64), nullable=False, primary_key=True)
    title = db.Column(db.String(64), nullable=False)

    schema = ServerSchema()

    def __init__(self, data):
        """Server model constructor."""
        self.endpoint = data.get('endpoint')
        self.title = data.get('title')

        db.session.add(self)
        db.session.commit()

    def __str__(self):
        """Return server instance as a string."""
        return f'{self.title}'

    def _set_stats_attrs(self, attrs):
        """Set attributes that display additional statistic."""
        setattr(self, 'min_match_time', attrs.min_match_time)
        setattr(self, 'max_match_time', attrs.max_match_time)
        setattr(self, 'avg_match_time', attrs.avg_match_time)
        setattr(self, 'total_matches', attrs.total_matches)
        setattr(self, 'total_players', attrs.total_players)

    @classmethod
    def get(cls, endpoint):
        """Retrieve single server instance from database."""
        server = db.session.query(cls).filter(cls.endpoint == endpoint).first()
        return server

    @classmethod
    def get_server_stats(cls, endpoint):
        """Retrieve single server instance with additional statistic."""
        result = db.session.query(
            cls, func.avg(Match.elapsed_time).label('avg_match_time'),
            func.max(Match.elapsed_time).label('max_match_time'),
            func.min(Match.elapsed_time).label('min_match_time'),
            func.count(Match.id).label('total_matches'),
            func.count(distinct(Scoreboard.player_nickname)).label('total_players'))\
            .join(Match)\
            .join(Match.players)\
            .group_by(cls.endpoint)\
            .filter(cls.endpoint == endpoint)\
            .first()

        if result:
            server = result.Server
            server._set_stats_attrs(result)
        else:
            server = cls.get(endpoint=endpoint)

        return server

    @classmethod
    def get_all(cls, order_by):
        """Retrieve all existing servers from database."""
        query = db.session.query(cls)
        if order_by == 'title':
            servers = query.order_by(cls.title)
        elif order_by == 'endpoint':
            servers = query.order_by(cls.endpoint)
        else:
            servers = query.order_by(func.random())

        return servers

    def update(self, new_title):
        """Update title of server."""
        if self.title != new_title:
            self.title = new_title
            db.session.commit()

        return self.title


class Player(db.Model, SchemaManager):
    """Player database representation."""

    __tablename__ = 'players'

    nickname = db.Column(db.String(128), nullable=False, primary_key=True)
    kills = db.Column(db.Integer, nullable=False, default=0)
    deaths = db.Column(db.Integer, nullable=False, default=0)
    assists = db.Column(db.Integer, nullable=False, default=0)
    matches = db.relationship('Scoreboard', back_populates='player')

    schema = PlayerSchema()

    def __init__(self, data):
        """Player model constructor."""
        self.nickname = data.get('nickname')

        db.session.add(self)
        db.session.commit()

    def __str__(self):
        """Return player instance as a string."""
        return f'{self.nickname}'

    def _set_stats_attrs(self, attrs):
        """Set attributes that display additional statistic."""
        setattr(self, 'total_matches', attrs.total_matches)
        setattr(self, 'max_kills_per_match', attrs.max_kills_per_match)
        setattr(self, 'max_deaths_per_match', attrs.max_deaths_per_match)
        setattr(self, 'max_assists_per_match', attrs.max_assists_per_match)
        setattr(self, 'max_match_time', attrs.max_match_time)
        setattr(self, 'min_match_time', attrs.min_match_time)

    @classmethod
    def get(cls, nickname):
        """Retrieve single player instance from database."""
        player = db.session.query(cls).filter(cls.nickname == nickname).first()
        return player

    @classmethod
    def get_player_stats(cls, nickname):
        """Retrieve single server instance with additional statistic."""
        result = db.session.query(
            cls, func.count(Match.id).label('total_matches'),
            func.max(Scoreboard.kills).label('max_kills_per_match'),
            func.max(Scoreboard.deaths).label('max_deaths_per_match'),
            func.max(Scoreboard.assists).label('max_assists_per_match'),
            func.max(Match.elapsed_time).label('max_match_time'),
            func.min(Match.elapsed_time).label('min_match_time'))\
            .join(Scoreboard)\
            .join(Match)\
            .group_by(cls.nickname)\
            .filter(cls.nickname == nickname)\
            .first()

        if result:
            player = result.Player
            player._set_stats_attrs(result)
        else:
            player = cls.get(nickname=nickname)

        return player

    @classmethod
    def get_all(cls, order_by, endpoint=None):
        """Retrieve ordered list of players."""
        if endpoint:
            players = db.session.query(cls) \
                .join(Scoreboard) \
                .join(Match) \
                .filter(Match.server_endpoint == endpoint)
        else:
            players = db.session.query(cls)

        if order_by == 'kills':
            players = players.order_by(Player.kills.desc())
        elif order_by == 'deaths':
            players = players.order_by(Player.deaths.desc())
        elif order_by == 'assists':
            players = players.order_by(Player.assists.desc())

        return players


class Scoreboard(db.Model):
    """Scoreboard database representation."""

    __tablename__ = 'scoreboards'

    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), primary_key=True)
    player_nickname = db.Column(db.String(128), db.ForeignKey('players.nickname'),
                                primary_key=True)
    match = db.relationship('Match', back_populates='players')
    player = db.relationship('Player', back_populates='matches')
    kills = db.Column(db.Integer, nullable=False, default=0)
    deaths = db.Column(db.Integer, nullable=False, default=0)
    assists = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, player_data, match_id):
        """Scoreboard model constructor."""
        self.player_nickname = player_data.get('nickname')
        self.kills = player_data.get('kills')
        self.deaths = player_data.get('deaths')
        self.assists = player_data.get('assists')
        self.match_id = match_id

        db.session.add(self)
        db.session.commit()


class Match(db.Model, SchemaManager):
    """Match database representation."""

    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    elapsed_time = db.Column(db.Interval, nullable=False)
    server_endpoint = db.Column(db.String(64), db.ForeignKey('servers.endpoint'))
    server = db.relationship('Server', backref=db.backref('matches', lazy='subquery'))
    players = db.relationship('Scoreboard', back_populates='match')

    schema = MatchSchema()

    def __init__(self, data):
        """Match model constructor."""
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')
        self.server_endpoint = data.get('server_endpoint')
        self.elapsed_time = self.end_time - self.start_time

        db.session.add(self)
        db.session.commit()

    def __str__(self):
        """Return match instance as a string."""
        return f'{self.title}'

    @classmethod
    def get_player_matches(cls, nickname):
        """Retrieve player matches from database."""
        query = db.session.query(cls).join(cls.players).filter(Player.nickname == nickname)
        matches = query.order_by(cls.end_time.desc())

        return matches

    @classmethod
    def get_server_matches(cls, endpoint):
        """Retrieve server matches ordered by end_time from database."""
        query = db.session.query(cls).join(Server).filter(Server.endpoint == endpoint)
        matches = query.order_by(cls.end_time.desc())

        return matches

    @classmethod
    def get(cls, id):
        """Retrieve single match instance from database."""
        match = db.session.query(cls).filter(cls.id == id).first()
        return match
