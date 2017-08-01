# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Vendor Order',
    'version': '10.0.1.0.0',
    'category': 'Purchase',
    'summary': """xls or ods report from ods template file to generate the
    purchase order report based on price list RMB, and list product, vendor
    product code, price unit, and total amount of each purchase order
    lines.""",
    "support": "support@elico-corp.com",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_vendor',
        'report_py3o'
    ],
    'data': [
        'report/trading_vendor_order.xml',
    ],
    'installable': True,
}
