# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Stock Delivery Note',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """The new module 'trading_stock_delivery_note'
    generate the xls or ods report from ods template file,
    This report show the order quantity and the delivery quantity of each lines
    inside sale order.""",
    'author': "Elico Corp",
    "support": "support@elico-corp.com",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_invoice',
        'report_py3o',
    ],
    'data': [
        'report/trading_stock_delivery_note.xml',
    ],
    'installable': True,
    'auto_install': False,
}
