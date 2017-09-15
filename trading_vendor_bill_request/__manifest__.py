# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Vendor Bill Request',
    'version': '10.0.1.0.0',
    'category': 'purchase',
    'summary': """Fields to compute total quantity of invoiced products
               usefull for purchase bill request and list the product.""",
    'support': 'support@elico-corp.com',
    'author': 'Elico Corp',
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_vendor',
        'report_py3o',
        'base_vat',
    ],
    'data': [
        'report/trading_vendor_bill_request.xml',
    ],
    'installable': True
}