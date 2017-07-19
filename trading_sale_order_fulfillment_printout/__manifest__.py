# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Sale Order Fulfillment Report',
    'version': '10.0.1.0.0',
    'category': 'Sale',
    'summary': """xls or ods report from ods template file to
    generate the trading sale order fulfillment report from
    sale order line.""",
    'author': "Elico Corp",
    'website': 'https://www.elico-corp.com',
    "support": "support@elico-corp.com",
    'license': 'AGPL-3',
    'depends': [
        'trading_sale',
        'report_py3o'
    ],
    'data': [
        'report/trading_sale_order_fulfillment_printout.xml',
    ],
    'installable': True,
    'auto_install': False,
}
