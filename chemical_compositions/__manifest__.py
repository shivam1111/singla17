# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Chemical Compositions',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Compositions Management',
    'description': """
    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_order','mill_purchase_order'],
    'data': [
            'data/ir_sequence_data.xml',
            'views/chemical_composition.xml',
            'security/ir.model.access.csv',
            'report/external_standard_layout.xml',
            'report/test_certificate.xml',
            'report/ir_actions_report.xml',

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
