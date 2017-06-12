# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trading Sale Custom Declaration",
    "summary": """Trading Sale Custom Declaration report for each
        sale orders (report_py3o)""",
    "version": "10.0.1.0.0",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": [
        "trading_sale",
        "report_py3o_multisheet",
    ],
    "data": [
        "demo/trading_sale_custom_declaration.xml",
    ],
    "installable": True,
}
