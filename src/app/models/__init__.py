"""Shooter stats database models."""


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
