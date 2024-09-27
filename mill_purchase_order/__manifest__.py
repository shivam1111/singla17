# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Order',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Purchase Orders Management',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_order'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/mill_purchase_order.xml',
        'views/res_partner.xml',
        'views/stock_view.xml',
        'views/heat_heat.xml',
        'views/material_grade.xml',
        'views/brokerage_report_view.xml',
        'report/ir_actions_report.xml',
        'report/brokerage_report.xml',
        'report/purchase_summary.xml',
        'report/heat_report.xml',
        'report/material_grade_report.xml',
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
