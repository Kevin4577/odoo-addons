# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Stock',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """The new module 'trading_stock' would provide custom management about custom check or so on.""",
    'author': "Elico corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'sale_stock'
    ],
    'data': [
        'views/stock_picking_view.xml'
    ],
    'installable': True
}
