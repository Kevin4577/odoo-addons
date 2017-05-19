# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Product HS Code China',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'summary': """This module specifies HS Code per product for China.""",
    'author': "Elico corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
                'sale_product_hs_code',
                ],
    'data': [
        'views/product_hs_code_view.xml',
        'views/product_template_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
