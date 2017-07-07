# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Sale Packaging Printout',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """Trading Sale Packaging Printout for each
    sale orders (report_py3o).""",
    'author': "Elico Corp",
    'support': "support@elico-corp.com",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'report_py3o',
        'trading_sale',
    ],
    'demo': [
        'demo/trading_sale_packaging_printout.xml',
    ],
    'installable': True,
    'auto_install': False,
}