# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Rent books'

    name = fields.Char('Title', required=True)