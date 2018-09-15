"""Marshmallow schemes for API representations."""

import re
from datetime import timedelta as td

from marshmallow import (
    Schema, fields, validates, ValidationError,
    validates_schema, post_dump)


class PlayerSchema(Schema):
    """Serializer schema for player JSON representation."""

    time_stats_fields = ['min_match_time', 'max_match_time']

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

    @post_dump
    def format_time_output(self, data):
        """Format time fields for output."""
        if all(self.time_stats_fields) in data:
            data['max_match_time'] = str(td(seconds=int(data.get('max_match_time', 0))))
            data['min_match_time'] = str(td(seconds=int(data.get('min_match_time', 0))))


class ServerSchema(Schema):
    """Serializer schema for server JSON representation."""

    time_stats_fields = ['min_match_time', 'max_match_time', 'avg_match_time']

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

    @post_dump
    def format_time_output(self, data):
        """Format time fields for output."""
        if all(self.time_stats_fields) in data:
            # TODO: create func for format time fields
            data['min_match_time'] = str(td(seconds=int(data.get('min_match_time', 0))))
            data['max_match_time'] = str(td(seconds=int(data.get('max_match_time', 0))))
            data['avg_match_time'] = str(td(seconds=int(data.get('avg_match_time', 0))))


class MatchSchema(Schema):
    """Serializer schema for match JSON representation."""

    id = fields.Int(dump_only=True)
    server_endpoint = fields.Str(required=True)
    start_time = fields.DateTime(format='%d.%m.%Y %H:%M:%S', required=True)
    end_time = fields.DateTime(format='%d.%m.%Y %H:%M:%S', required=True)
    elapsed_time = fields.TimeDelta(dump_only=True)
    players = fields.Nested(PlayerSchema, many=True, exclude='nickname')

    @validates_schema
    def validate_time(self, data):
        """Validate match start and end time."""
        if data['start_time'] > data['end_time']:
            message = 'The start time must be earlier than the end time.'
            raise ValidationError(message, 'start_time')

    @post_dump
    def format_elapsed_time_output(self, data):
        """Format elapsed time field for output."""
        data['elapsed_time'] = str(td(seconds=int(data.get('elapsed_time', 0))))
