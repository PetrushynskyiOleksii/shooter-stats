"""Collections of helpers functions."""

from flask import url_for


def paginate_response(data, page=1):
    """Return formatted responses with pagination data."""
    pagination = data.paginate(page, per_page=25, error_out=False)
    prev = None
    if pagination.has_prev:
        prev = url_for('shooter.get_servers', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('shooter.get_servers', page=page + 1)

    response = {
        'servers': [obj.to_dict() for obj in pagination.items],
        'prev': prev,
        'next': next,
        'count': pagination.total
    }
    return response
