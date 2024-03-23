# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceApi(http.Controller):
#     @http.route('/invoice_api/invoice_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_api/invoice_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_api.listing', {
#             'root': '/invoice_api/invoice_api',
#             'objects': http.request.env['invoice_api.invoice_api'].search([]),
#         })

#     @http.route('/invoice_api/invoice_api/objects/<model("invoice_api.invoice_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_api.object', {
#             'object': obj
#         })
