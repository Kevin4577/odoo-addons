# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Sale',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'summary': """Sales Export trading common methods and information.""",
    'author': "Elico Corp",
    'website': 'https://www.elico-corp.com',
    "support": "support@elico-corp.com",
    'license': 'AGPL-3',
    'depends': [
        'sale_product_hs_code_china',
        'stock_package_volume_weight',
        'stock_packaging_lot',
        'stock_picking_invoice_reference',
        'account_invoice_customer_reference',
        'sale_order_dates'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/decimal_product.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
