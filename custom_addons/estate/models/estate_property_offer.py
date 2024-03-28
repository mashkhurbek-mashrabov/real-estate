from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float("Price", required=True)
    validity = fields.Integer("Offer Validity (days)", required=True, default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    status = fields.Selection(string="Status", copy=False,
                              selection=[("accepted", 'Accepted'), ("refused", 'Refused')])
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", required=True, ondelete='cascade')
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type",
                                       related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ("check_positive_offer_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    @api.model
    def create(self, vals):
        best_offer = self.env['estate.property'].browse(vals['property_id']).best_offer
        if vals['price'] < best_offer:
            raise UserError(
                f"Can't create an offer with a price less than the best offer! \n The best offer is: {best_offer}")
        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super(PropertyOffer, self).create(vals)

    @api.depends('validity', 'create_date')
    def _compute_deadline_date(self):
        for record in self:
            initial_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(initial_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            initial_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - initial_date).days

    def action_set_accepted_status(self):
        for record in self:
            if self._is_valid_deal(record.property_id.state):
                raise UserError(_("The offer cannot be accepted on a closed deal."))
            elif record.status == 'refused':
                raise UserError(_("The property offer has already been refused"))
            elif record.status == 'accepted':
                raise UserError(_("The property offer has already been accepted"))
            else:
                record.property_id.buyer_id = record.partner_id
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.selling_price = record.price
        return True

    def action_set_refused_status(self):
        for record in self:
            if self._is_valid_deal(record.property_id.state):
                raise UserError(_("The offer cannot be rejected on a closed deal.."))
            if record.property_id.buyer_id == record.partner_id and record.property_id.selling_price == record.price:
                record.property_id.buyer_id = None
                record.property_id.state = 'new'
                record.property_id.selling_price = 0
            record.status = 'refused'
            return True

    @staticmethod
    def _is_valid_deal(state):
        return state in ['sold', 'canceled', 'offer_accepted']
