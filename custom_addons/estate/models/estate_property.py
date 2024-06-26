from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = "id desc"

    salesperson_id = fields.Many2one(comodel_name='res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', string='Offers', inverse_name="property_id")
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False,
                                    default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    best_offer = fields.Float("Best Offer", compute="_compute_best_offer")
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area Number (sqm)")
    facades = fields.Integer("Facades Number")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string='Orientation',
                                          selection=[('north', 'North'),
                                                     ('south', 'South'),
                                                     ('east', 'East'),
                                                     ('west', 'West'),
                                                     ],
                                          help="Garden Orientation")
    total_area = fields.Integer("Total Area (sqm)", compute='_compute_total_area')
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(string='State', required=True, copy=False, default='new',
                             selection=[('new', 'New'),
                                        ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')
                                        ])

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if not (record.state in ['new', 'canceled']):
                raise UserError(f"Removing {record.state} state isn't allowed!")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = None
        else:
            self.garden_area = self.garden_area or 10
            self.garden_orientation = self.garden_orientation or 'north'

    @api.constrains("expected_price", "selling_price")
    def _check_property_pricing(self):
        for record in self:
            if record.state != "new" and float_compare(record.selling_price, record.expected_price * 0.9,
                                                       2) < 0:
                raise ValidationError(message="The selling price can't be lower than 90% the expected price!")

    def action_set_sold_state(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled property cannot be sold and a sold"))
            elif record.state == 'sold':
                raise UserError(_("The property is already sold"))
            else:
                record.state = 'sold'
        return True

    def action_set_canceled_state(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold property cannot be canceled"))
            elif record.state == 'canceled':
                raise UserError(_("The property is already canceled"))
            else:
                record.state = 'canceled'
        return True
