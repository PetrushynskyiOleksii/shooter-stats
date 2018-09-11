"""Marshmallow schemes for API representations."""

import re

from marshmallow import (
    Schema, fields, validates, ValidationError, validates_schema
)


class PlayerSchema(Schema):
    """Serializer schema for player JSON representation."""

    nickname = fields.Str(required=True)
    player_nickname = fields.Str(dump_only=True)
    kills = fields.Int()
    deaths = fields.Int()
    assists = fields.Int()
    kda = fields.Method('get_kda', dump_only=True)
    total_matches = fields.Int(dump_only=True)
    max_kills_per_match = fields.Int(dump_only=True)
    max_deaths_per_match = fields.Int(dump_only=True)
    max_assists_per_match = fields.Int(dump_only=True)
    max_match_time = fields.TimeDelta(dump_only=True)
    min_match_time = fields.TimeDelta(dump_only=True)

    def get_kda(self, obj):
        """Return KDA value."""
        try:
            kda = (obj.kills + obj.assists) / obj.deaths
        except ZeroDivisionError:
            kda = obj.kills + obj.assists

        return round(kda, 2)

    @validates('nickname')
    def validate_nickname(self, nickname):
        """Validate player nickname value."""
        if not re.fullmatch(r'[a-zA-Z0-9]+', nickname):
            message = 'Nickname must contains only chars or digits.'
            raise ValidationError(message)


class ServerSchema(Schema):
    """Serializer schema for server JSON representation."""

    endpoint = fields.Str(required=True)
    title = fields.Str(required=True)
    total_matches = fields.Int(dump_only=True)
    total_players = fields.Int(dump_only=True)
    min_match_time = fields.TimeDelta(dump_only=True)
    max_match_time = fields.TimeDelta(dump_only=True)
    avg_match_time = fields.TimeDelta(dump_only=True)

    @validates('endpoint')
    def validate_endpoint(self, endpoint):
        """Validate endpoint value."""
        if not re.fullmatch(r'^.+-\d{4,5}', endpoint):
            message = 'Endpoint must match template: domain-port.'
            raise ValidationError(message)


class MatchSchema(Schema):
    """Serializer schema for match JSON representation."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    server_endpoint = fields.Str(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    elapsed_time = fields.TimeDelta(dump_only=True)
    players = fields.Nested(PlayerSchema, many=True, exclude='nickname')

    @validates_schema
    def validate_time(self, data):
        """Validate match start and end time."""
        if data['start_time'] > data['end_time']:
            message = 'The start time must be earlier than the end time.'
            raise ValidationError(message, 'start_time')
