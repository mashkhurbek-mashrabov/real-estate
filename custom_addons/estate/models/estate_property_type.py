from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used for manual ordering!")

    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'The type name must be unique!')]