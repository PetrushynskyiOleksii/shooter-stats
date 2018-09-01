"""Stats models for database representation."""

from app import db


class GameMod(db.Model):
    """Server database representation."""

    __tablename__ = 'game_mods'

    title = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, data):
        """Game mods model constructor."""
        self.title = data.get('title')
        self.description = data.get('description')

    def save(self):
        """Save game mod instance in database."""
        # TODO: abstract method
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete game mod instance from database."""
        # TODO: abstract method
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_gamemod(id):
        """Retrieve particular game mod instance."""
        return GameMod.query.get(id)

    def __repr__(self):
        """Return game mod instance as a string."""
        return f'{self.title}'
