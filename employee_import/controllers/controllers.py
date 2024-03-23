# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeImport(http.Controller):
#     @http.route('/employee_import/employee_import/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_import/employee_import/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_import.listing', {
#             'root': '/employee_import/employee_import',
#             'objects': http.request.env['employee_import.employee_import'].search([]),
#         })

#     @http.route('/employee_import/employee_import/objects/<model("employee_import.employee_import"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_import.object', {
#             'object': obj
#         })
