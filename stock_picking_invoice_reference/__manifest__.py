# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking Invoice Reference',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """The new module 'stock_picking_invoice_reference' specifies 
    the invoice reference for each delivery order.""",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_stock_shipping',
        'account_invoice_customer_reference',
    ],
    'data': [
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
