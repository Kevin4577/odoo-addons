# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Export Purchase Order Printout',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """Sale Export Purchase Order Printout report for each
    sale orders (report_py3o).""",
    'author': "Elico Corp",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'base_sale_export',
        'report_py3o',
    ],
    'demo': [
        'demo/sale_export_purchase_order_printout.xml',
    ],
    'installable': True,
    'auto_install': False,
}
