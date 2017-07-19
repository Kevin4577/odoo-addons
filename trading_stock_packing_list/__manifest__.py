# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Stock Packing List',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'summary': """xls or ods report from ods template file with each product
    information inside account invoice.""",
    'author': "Elico Corp",
    "support": "support@elico-corp.com",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_invoice',
        'report_py3o',
    ],
    'data': [
        'report/trading_stock_packing_list.xml',
    ],
    'installable': True,
    'auto_install': False,
}
