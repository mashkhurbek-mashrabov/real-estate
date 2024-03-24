from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"

    price = fields.Float("Price", required=True)
    validity = fields.Integer("Offer Validity (days)", required=True, default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    status = fields.Selection(string="Status", no_copy=True,
                              selection=[("accepted", 'Accepted'), ("refused", 'Refused')])
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", required=True)

    @api.depends('validity', 'create_date')
    def _compute_deadline_date(self):
        for record in self:
            initial_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(initial_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            initial_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - initial_date).days