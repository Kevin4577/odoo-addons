# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order Line Received Quantity Refund',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'summary': """This module improves the generation rule of received quantity
    of each purchase order line.""",
    "support": "support@elico-corp.com",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
         'views/purchase_view.xml',
    ],
    'installable': True,
}
