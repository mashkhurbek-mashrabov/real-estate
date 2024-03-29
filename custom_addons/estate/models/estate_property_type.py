from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used for manual ordering!")
    property_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    offer_ids = fields.One2many(string="Property Offer",
                                comodel_name="estate.property.offer",
                                inverse_name='property_type_id')
    offer_count = fields.Integer(string="Number Of Offers", compute="_compute_number_of_offers")

    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'The type name must be unique!')]

    @api.depends("offer_ids")
    def _compute_number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
