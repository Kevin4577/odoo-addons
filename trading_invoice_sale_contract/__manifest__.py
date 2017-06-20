# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Invoice Sale Contract',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'summary': """The new module 'trading_invoice_sale_contract' generate
    the xls or ods report from ods template file with each product
    information inside sale order""",
    'author': "Elico Corp",
    "support": "support@elico-corp.com",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_invoice',
        'report_py3o',
    ],
    'data': [
        'report/trading_invoice_sale_contract.xml',
    ],
    'installable': True,
    'auto_install': False,
}
