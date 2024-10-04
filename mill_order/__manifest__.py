# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mill Order',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Orders Management',
    'description': """
    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/mill_menus.xml',
        'views/mill_order_view.xml',
        'data/ir_sequence_data.xml',
        'report/report_orders_list.xml',
        'report/ir_actions_report.xml',
        'report/mill_order_report_view.xml',

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
