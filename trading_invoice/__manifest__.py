# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trading Invoice",
    "version": "10.0.1.1.0",
    "summary": """Trading Invoice common methods and information""",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": [
        "stock_package_volume_weight",
        "stock_packaging_lot",
        "sale_product_hs_code_china",
        "product_class",
        "stock_picking_invoice_reference",
        "sale_order_dates"
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/decimal_case_lot.xml',
        'data/decimal_product.xml',
    ],
    "installable": True,
}
