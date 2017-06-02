# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Package Volume Weight",
    "version": "10.0.1.0.0",
    "summary": """This module extends the Package and Package Types to
                    add extra fields related to product conditioning.""",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": ["stock"],
    "data": [
        "views/product_packaging_view.xml",
        "views/stock_quant_package_view.xml",
    ],
    "installable": True,
}
