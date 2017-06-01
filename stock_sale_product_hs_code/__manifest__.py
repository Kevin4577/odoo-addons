# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Sale Product HS Code',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """This module extends the model stock production lot to add
    extra fields related to product conditioning.""",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_production_lot_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
