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


class GameMod(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'game_mods'

    title = db.Column(db.String(10), nullable=False)
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


class Server(db.Model, BaseManager):
    """Server database representation."""

    __tablename__ = 'servers'

    id = db.Column(db.SmallInteger, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    endpoint = db.Column(db.String(128), nullable=False)
    total_matches_played = db.Column(db.Integer)
    # TODO: avg & max played per day

    def __init__(self, data):
        """Post model constructor."""
        self.title = data.get('title')
        self.endpoint = data.get('endpoint')
        self.total_matches_played = 0

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
