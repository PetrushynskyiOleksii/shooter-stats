"""Marshmallow schemes for API representations."""

from marshmallow import Schema, fields


class PlayerSchema(Schema):
    """Serializer schema for player JSON representation."""

    nickname = fields.Str(required=True)
    kills = fields.Int()
    deaths = fields.Int()
    assists = fields.Int()
    kda = fields.Method('get_kda')

    def get_kda(self, obj):
        """Return KDA value."""
        try:
            kda = (obj.kills + obj.assists) / obj.deaths
        except ZeroDivisionError:
            kda = obj.kills + obj.assists

        return round(kda, 2)


player_schema = PlayerSchema()


class ServerSchema(Schema):
    """Serializer schema for server JSON representation."""

    endpoint = fields.Str(required=True)  # TODO: validation
    title = fields.Str(required=True)
    total_matches = fields.Method('get_total_matches', dump_only=True)
    # TODO: total players

    def get_total_matches(self, obj):
        """Return count of matches played on server."""
        return len(obj.matches)


server_schema = ServerSchema()


class MatchSchema(Schema):
    """Serializer schema for match JSON representation."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    server_endpoint = fields.Nested(ServerSchema, only='endpoint', attribute='server')
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    elapsed_time = fields.Method('get_elapsed_time', dump_only=True)
    scoreboard = fields.Nested(PlayerSchema, many=True)

    def get_elapsed_time(self, obj):
        """Return elapsed time during match."""
        return str(obj.end_time - obj.start_time)

    # TODO: validate time -> end_time>start_time


match_schema = MatchSchema()
