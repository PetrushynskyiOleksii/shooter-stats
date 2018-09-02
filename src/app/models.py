"""Stats models for database representation."""

from app import db


class BaseManager(object):
    """Base query manager."""

    def save(self):
        """Save instance in database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete instance from database."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update existing instance in database."""
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()


mods = db.Table(
    'mods',
    db.Column('gamemod_id', db.Integer, db.ForeignKey('gamemod.id'), primary_key=True),
    db.Column('server_id', db.Integer, db.ForeignKey('server.id'), primary_key=True)
)


class Server(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(128), nullable=False, unique=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    mods = db.relationship('GameMod', secondary=mods, lazy='subquery')

    def __init__(self, data):
        """Post model constructor."""
        self.endpoint = data.get('endpoint')
        self.title = data.get('title')

    @staticmethod
    def get_all():
        """Return all servers instances from database."""
        return Server.query.all()

    @staticmethod
    def get_server(id):
        """Retrieve particular server instance."""
        return Server.query.get(id)

    def __repr__(self):
        """Return server instance as a string."""
        return f'{self.title} ({self.id})'


class GameMod(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'game_mods'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, data):
        """Game mods model constructor."""
        self.title = data.get('title')
        self.description = data.get('description')

    @staticmethod
    def get_gamemod(id):
        """Retrieve particular game mod instance."""
        return GameMod.query.get(id)

    def __repr__(self):
        """Return game mod instance as a string."""
        return f'{self.title}'


class Match(db.Model, BaseManager):
    """Match database representation."""

    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(48), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    # TODO: scoreboard (many to many - player)
    # TODO: server (foreign key - server)

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
