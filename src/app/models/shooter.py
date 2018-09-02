"""Stats models for database representation."""

from . import db, BaseManager


class Server(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'server'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(128), nullable=False, unique=True)
    title = db.Column(db.String(64), nullable=False)

    def __init__(self, data):
        """Post model constructor."""
        self.endpoint = data.get('endpoint')
        self.title = data.get('title')

    def __repr__(self):
        """Return server instance as a string."""
        return f'{self.title} ({self.id})'

    @staticmethod
    def get_all():
        """Return all servers instances from database."""
        return Server.query.all()

    @staticmethod
    def get_server(id):
        """Retrieve particular server instance."""
        return Server.query.get(id)


class Match(db.Model, BaseManager):
    """Match database representation."""

    __tablename__ = 'match'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(48), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    scoreboard = db.relationship('MatchPlayer', backref='match', lazy=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    server = db.relationship('Server', backref=db.backref('matches', lazy='dynamic'))

    def __init__(self, data):
        """Match model constructor."""
        self.title = data.get('title')
        self.start_time = data.get('start_time')

    @staticmethod
    # TODO
    def get_match(id):
        """Retrieve particular match instance."""
        return Match.query.get(id)

    @staticmethod
    def get_all_server_matches(id, server):
        """Return all matches played on server."""
        # TODO
        pass

    def __repr__(self):
        """Return match instance as a string."""
        return f'{self.title}'
