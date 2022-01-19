from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'A tag for property, i.e. cozy or renovated...'
    _order = 'name'
    _sql_constraints = [
        ('unique_tag_name', 'unique (name)', "The property tag name must be unique!")
    ]

    name = fields.Char(required=True)
    color = fields.Integer()