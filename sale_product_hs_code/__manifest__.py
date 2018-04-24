# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Product HS Code',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'summary': """This module specifies HS Code per product.""",
    'support': 'support@elico-corp.com',
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'security/product_hs_code_security.xml',
        'security/ir.model.access.csv',
        'views/product_hs_code_view.xml',
        'views/product_template_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}