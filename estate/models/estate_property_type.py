from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type, i.e. house, apartment... '
    _order = 'sequence, name'
    _sql_constraints = [
        ('unique_type_name', 'unique (name)', 'The property type name must be unique!')
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name='estate.property',
                                   inverse_name='property_type_id',
                                   string='Properties')
    sequence = fields.Integer()