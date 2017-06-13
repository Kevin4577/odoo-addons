# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking Partner Invisible',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """This module specifies Stock Picking Partner Invisible.""",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'security/stock_security.xml',
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
