# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Stock Shipping',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """This module specifies Trading Stock shipping information.""",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'sale_stock'
    ],
    'data': [
        'security/stock_security.xml',
        'security/ir.model.access.csv',
        'views/shipping_view.xml',
        'views/stock_picking_view.xml'
    ],
    'installable': True
}
