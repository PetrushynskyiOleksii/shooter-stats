"""Marshmallow schemes for API representations."""

from marshmallow import Schema, fields


class ServerSchema(Schema):
    """Serializer schema for server JSON representation."""

    endpoint = fields.Str(required=True)  # TODO: validation
    title = fields.Str(required=True)


server_schema = ServerSchema()
servers_schema = ServerSchema(many=True)


class MatchServer(Schema):
    """Serializer schema for match JSON representation."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    server = fields.Nested(ServerSchema, dump_only=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

    # scoreboard = db.relationship('MatchPlayer', backref='match', lazy=True)
    # TODO: preload elapsed time


match_schema = MatchServer()
matches_schema = MatchServer(many=True)
