"""Collections of API endpoints."""

from flask import Blueprint

shooter_api = Blueprint('shooter', __name__)

from . import players, servers, matches
