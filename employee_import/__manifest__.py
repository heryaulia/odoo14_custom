# -*- coding: utf-8 -*-
{
    'name': "Employee Import",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Hery Aulia Rahmad",
    'website': "http://h3ry.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'queue_job'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/email_confirmation_data.xml',
        'views/employee_import_views.xml',
    ],
}
