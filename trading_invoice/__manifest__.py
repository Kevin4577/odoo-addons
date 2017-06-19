# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trading Invoice",
    "version": "10.0.1.0.0",
    "summary": """The new module provide methods for Invoice report modules
               with the data. Those methods be reused by several modules,
               in order to improve the maintainability of project modules.""",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": ["stock_package_volume_weight",
                "stock_packaging_lot",
                "trading_stock_shipping",
                "sale_product_hs_code_china",
                ],
    "installable": True,
}
