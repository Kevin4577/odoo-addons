# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Export Customs Declaration Printout",
    "summary": """Sale Export Customs Declaration Printout report for each
        sale orders (report_py3o)""",
    "version": "10.0.1.0.0",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": [
        "base_sale_export",
        "report_py3o_multisheet",
    ],
    "data": [
        "demo/sale_export_customs_declaration_printout.xml",
    ],
    "installable": True,
}
