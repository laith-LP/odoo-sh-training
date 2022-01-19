from odoo import fields, models, api


class Session(models.Model):
    _name = 'academy.session'
    _description = 'A lecture session for a course'

    name = fields.Char(string='Name')
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    duration = fields.Integer(string='Duration')
    number_of_seats = fields.Integer(string='Available Seats')
    instructor_id = fields.Many2one(comodel_name='res.partner', string='Instructor')

    course_id = fields.Many2one(comodel_name='academy.course', string='Related Course', required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    instructored_session_ids = fields.One2many(comodel_name='academy.session',
                                               inverse_name='instructor_id',
                                               string='Instructored Sessions')