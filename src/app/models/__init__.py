"""Shooter stats database models."""

from app import db


class BaseManager(object):
    """Base query manager."""

    def _save(self):
        """Save instance in database."""
        db.session.add(self)
        db.session.commit()
