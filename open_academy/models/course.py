from datetime import timedelta

from odoo import fields, models


class Course(models.Model):
    _name = 'academy.course'

    title = fields.Char(string="Title", required=True)

    description = fields.Text(string='Description')

    states = fields.Selection(
        [('default', 'Default State'),
         ('state1', 'State 1'),
         ('state2', 'State 2')],
        string='States', default='default'
    )

    responsible = fields.Many2one(comodel_name='res.users', string='Responsible')

    def print_course_title(self):
        print(self.title)

    def print_course_description(self):
        print(self.description)