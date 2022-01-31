# -*- coding: utf-8 -*-

from odoo import models, fields, api

from . import utils


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    # _sql_constraints = [
    #     ('Unique Book Name', 'UNIQUE (name)', 'Book name must be unique.')
    # ]

    ref_id = fields.Char()
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    # days_since_release = fields.Integer(default=0)
    publisher_id = fields.Many2one(comodel_name='res.partner')
    author_ids = fields.Many2many('res.partner', string='Authors')
    state = fields.Selection(selection='get_state_selection', string='State', default="coming_soon")
    price = fields.Integer(store=True, index=True)
    # price_range_id = fields.Many2one(comodel_name='library.book.price.range')
    description = fields.Html('Description', sanitize=True, strip_style=False)

    def get_state_selection(self):
        return [('coming_soon', 'Coming Soon'),
                ('available', 'Available'),
                ('lost', 'Lost')]

    # TODO rating = fields.Integer()

    @api.model
    def sync_books(self):
        print("Syncing Books...")
        utils.scan_file(self)
        print("Syncing Completed.")

    def make_available(self):
        self.write({'state': 'available'})

    def book_coming_soon(self):
        self.write({'state': 'coming_soon'})

    def make_lost(self):
        self.write({'state': 'lost'})


class LibraryBookPriceRange(models.Model):
    _name = 'library.book.price.range'
    _description = 'Price range for books'

    name = fields.Char(required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        comodel_name='library.book', inverse_name='publisher_id', string='Published Books')

    # @api.onchange('date_release')
    # def compute_days_since_release(self):
    #     for book in self:
    #         if book.date_release:
    #             days = (fields.Date.today() - self.date_release).days
    #             if days > 0:
    #                 book.days_since_release = days
    #             else:
    #                 book.days_since_release = 0
    #         else:
    #             book.days_since_release = 0
    #
    # @api.onchange('price')
    # def compute_price_range(self):
    #     for book in self:
    #         if book.price:
    #             if book.price == 0:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', 'Unknown')])
    #             elif 1 <= book.price <= 20:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', '1-20')])
    #             elif 20 <= book.price <= 40:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', '20-40')])
    #             elif 40 <= book.price <= 60:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', '40-60')])
    #             elif 60 <= book.price <= 80:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', '60-80')])
    #             elif 80 <= book.price <= 100:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', '80-100')])
    #             else:
    #                 book.price_range_id = self.env['library.book.price.range'].search([('name', '=', 'Above 100')])