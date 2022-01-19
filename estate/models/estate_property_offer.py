from datetime import timedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer to buy the property'
    _order = 'price desc'
    _sql_constraints = [
        ('positive_price', 'CHECK (price >= 0)', 'Offer price must be positive.')
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'),
                   ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Buyer', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    def action_accept(self):
        self.ensure_one()
        self.status = 'accepted'
        all_properties = self.env['estate.property'].search([])

        for rec in all_properties:
            # TODO: This check can be removed if we searched on the right property.
            if rec == self.property_id:
                rec.partner_id = self.partner_id
                rec.selling_price = self.price
                rec.state = 'sold'

    def action_refuse(self):
        self.status = 'refused'

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            start_date = fields.Date.today()
            if rec.create_date:
                start_date = rec.create_date
            rec.date_deadline = start_date + timedelta(rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.create_date:
                delta = rec.date_deadline - fields.Date.today()
                rec.validity = delta.days