# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Class',
    'version': '10.0.1.0.0',
    'category': 'Product',
    'summary': """This module specifies product classes,
    and generates the product code per product.""",
    'author': "Elico corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'sale',
        'purchase'
    ],
    'data': [
        'security/product_class_security.xml',
        'security/ir.model.access.csv',
        'views/stock_menu_views.xml',
        'views/product_stage_view.xml',
        'views/product_line_view.xml',
        'views/product_class_view.xml',
        'views/product_family_view.xml',
        'views/product_template_view.xml',
    ],
    'demo': [
        'demo/product_stage_demo.xml',
        'demo/product_line_demo.xml',
        'demo/product_class_demo.xml',
        'demo/product_family_demo.xml',
        'demo/product_template_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
