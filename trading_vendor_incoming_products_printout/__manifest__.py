# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Vendor Incoming Products Printout',
    'version': '10.0.1.0.0',
    'category': 'Purchase',
    'summary': """The new module 'trading_vendor_incoming_products_printout'
    inherit the model 'stock.move', and add necessary fields for each stock
    move of related incoming products for each purchase lines. It allows user
    to generate incoming products report for all products, which was still
    waiting for receiving.""",
    "support": "support@elico-corp.com",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'product_class',
        'report_py3o',
        'trading_vendor'
    ],
    'data': [
        'views/purchse_view.xml',
        'report/trading_vendor_incoming_products_printout.xml'
    ],
    'installable': True,
}
