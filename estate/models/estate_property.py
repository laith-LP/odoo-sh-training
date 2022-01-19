from datetime import timedelta

from odoo.exceptions import UserError, ValidationError

from odoo import models, fields, api, _


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Represents a property for selling'
    _order = 'id desc'
    _sql_constraints = [
        ('positive_expected_price', 'CHECK (expected_price >= 0)', 'Expected price must be positive.'),
        ('positive_selling_price', 'CHECK (selling_price >= 0)', 'Selling price must be positive.')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char(index=True)
    date_availability = fields.Date(copy=False, default=fields.Date.today() + timedelta(days=90))
    # TODO: SEE TODOS, a lot of the logic is broken...
    expected_price = fields.Float(required=True)
    best_price = fields.Integer(string='Best Offer', compute='_compute_best_price')
    selling_price = fields.Float(readonly=True, copy=False)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        # Selling price should be at least 90% of the expected price.
        if self.expected_price and self.selling_price < (self.expected_price * 90 / 100):
            raise ValidationError(_('The selling price must be at least 90% of the expected price!'
                                    'You must reduce the expected price or increase the selling price'
                                    'if you want to accept the offer.'))

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    # Should be available only if 'garden' is True
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('east', 'East'),
                   ('west', 'West'),
                   ('north', 'North'),
                   ('south', 'South')],
        string='Garden Orientation',
        help='The direction of the garden relative to the property.')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'),
                   ('received', 'Offer Received'),
                   ('accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('canceled', 'Canceled')],
        required=True, copy=False, default='new', string='Status')
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string='Property Type')
    user_id = fields.Many2one(comodel_name='res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string='Offers')

    def action_sold(self):
        self.ensure_one()
        if self.state != 'canceled':
            self.state = 'sold'
        else:
            raise UserError(_(f"The canceled property {self.name} cannot be sold!"))

    def action_cancel(self):
        self.ensure_one()
        if self.state != 'sold':
            self.state = 'canceled'
        else:
            raise UserError(_(f"The sold property {self.name} cannot be canceled!"))

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            max_offer = 0
            for offer in self.offer_ids:
                if offer.price > max_offer:
                    max_offer = offer.price
            rec.best_price = max_offer

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 0
        self.garden_orientation = ''

        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    # TODO: set selling price to zero when there are no offers!
    # This methods works but doesn't store the selling_price value after saving the form view.
    @api.onchange('best_price')
    def _onchange_best_price(self):
        if self.best_price == 0:
            self.selling_price = 0