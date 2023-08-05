from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    intervention_uid = fields.String(validate=not_blank, required=True)
    preferred_term = fields.String(validate=not_blank, required=True)
    intervention_type = fields.String()
    pharm_action_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
