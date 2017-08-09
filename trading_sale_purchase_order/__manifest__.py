# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Sale Purchase Order',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """Trading Sale Purchase Order report for each
    sale orders (report_py3o).""",
    'author': "Elico Corp",
    'support': "support@elico-corp.com",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_sale',
        'report_py3o',
    ],
    'data': [
        'report/trading_sale_purchase_order.xml',
    ],
    'installable': True,
    'auto_install': False,
}
