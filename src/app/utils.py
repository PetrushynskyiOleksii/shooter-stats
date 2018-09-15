"""Collections of helpers functions."""

from flask import request
from datetime import timedelta


def paginate_response(data, page=1):
    """Return formatted responses with pagination data."""
    pagination = data.paginate(page, per_page=25, error_out=False)
    prev = None
    if pagination.has_prev:
        prev = f'{request.path}?page={page-1}'
    next = None
    if pagination.has_next:
        next = f'{request.path}?page={page+1}'

    response = {
        'objects': [obj.to_dict() for obj in pagination.items],
        'prev': prev,
        'next': next,
        'count': pagination.total
    }
    return response


def format_time(time):
    """Return formatted time."""
    duration = timedelta(seconds=int(time))
    return str(duration)
