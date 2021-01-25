from marshmallow import Schema, fields, EXCLUDE


class FlightPlan(Schema):
    ICAO = fields.List(fields.String(), required=True)
    DateTime = fields.List(fields.String(), required=True)

    class Meta:
        unknown = EXCLUDE
