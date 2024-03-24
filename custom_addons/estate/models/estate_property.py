from odoo import models, fields, api


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'

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
