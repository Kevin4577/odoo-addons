# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Base Sale Export',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """Sales Export trading common methods and information.""",
    'author': "Elico Corp",
    'website': 'https://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'sale_product_hs_code_china',
        'stock_shipping',
        'stock_package_volume_weight',
        'stock_packaging_lot'
    ],
    'installable': True,
    'auto_install': False,
}
