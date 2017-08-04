# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Vendor Order Summary',
    'version': '10.0.1.0.0',
    'category': 'purchase',
    'summary': """This module to add vendor product code for each purchase
    order lines. """,
    'support': 'support@elico-corp.com',
    'author': 'Elico Corp',
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_vendor',
        'report_py3o',
        'sale',
    ],
    'data': [
        'report/trading_vendor_order_summary.xml',
        'views/trading_vendor_order_summary_view.xml',
    ],
    'installable': True
}
