# -*- coding: utf-8 -*-
# from odoo import http


# class MyScaffold(http.Controller):
#     @http.route('/my_scaffold/my_scaffold/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_scaffold/my_scaffold/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_scaffold.listing', {
#             'root': '/my_scaffold/my_scaffold',
#             'objects': http.request.env['my_scaffold.my_scaffold'].search([]),
#         })

#     @http.route('/my_scaffold/my_scaffold/objects/<model("my_scaffold.my_scaffold"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_scaffold.object', {
#             'object': obj
#         })
