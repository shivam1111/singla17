# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Production Order',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Produciton Management',
    'description': """
    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_purchase_order'],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/production_order.xml',
        'views/heat_view.xml',
        'views/mill_production_view.xml',
        'report/ir_actions_report.xml',
        'report/production_order_report.xml',


    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
