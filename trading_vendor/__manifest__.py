# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Vendor',
    'version': '10.0.1.0.0',
    'category': 'Purchase',
    'summary': """Common methods and fields for vendor trading printouts""",
    "support": "support@elico-corp.com",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'product_class'
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
