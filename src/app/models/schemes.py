"""Marshmallow schemes for API representations."""

from marshmallow import Schema, fields


class PlayerSchema(Schema):
    """Serializer schema for player JSON representation."""

    # TODO: add order property in meta class

    nickname = fields.Str(required=True)
    kills = fields.Int()
    deaths = fields.Int()
    assists = fields.Int()

    # TODO: pre dump KDA property


players_schema = PlayerSchema(many=True)
player_schema = PlayerSchema()


class ServerSchema(Schema):
    """Serializer schema for server JSON representation."""

    endpoint = fields.Str(required=True)  # TODO: validation
    title = fields.Str(required=True)


server_schema = ServerSchema()
servers_schema = ServerSchema(many=True)


class MatchSchema(Schema):
    """Serializer schema for match JSON representation."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    server = fields.Nested(ServerSchema, dump_only=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    scoreboard = fields.Nested(PlayerSchema, many=True)
    # TODO: preload elapsed time
    # TODO: validate time -> end_time>start_time


match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)  # FIXME
