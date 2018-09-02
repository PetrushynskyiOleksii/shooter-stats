"""Marshmallow schemes for API representations."""

from marshmallow import Schema, fields


class ServerSchema(Schema):
    """Schema for server JSON representation."""

    id = fields.Integer(dump_only=True)  # read only field
    endpoint = fields.Str(required=True)  # TODO: validation
    title = fields.Str(required=True)


server_schema = ServerSchema()
