# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Export Customs Declaration Items Printout',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'summary': """Sale export customs declaration items printout for each
    sale orders (report_py3o).""",
    'author': "Elico Corp",
    "support": "support@elico-corp.com",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'report_py3o',
        'trading_sale'
    ],
    'data': [
        'report/sale_export_customs_declaration_items_printout.xml'
    ],
    'installable': True,
    'auto_install': False,
}
