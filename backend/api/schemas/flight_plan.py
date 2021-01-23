from marshmallow import Schema, fields, EXCLUDE


class FlightPlan(Schema):
    fromICAO = fields.List(fields.String(), required=True)
    toICAO = fields.List(fields.String(), required=True)

    class Meta:
        unknown = EXCLUDE
