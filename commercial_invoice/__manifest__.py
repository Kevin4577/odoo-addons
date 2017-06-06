# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Commercial Invoice",
    "summary": """This module would generate commercial invoice report for
        each sale orders, and supported by the OCA report enginee module named
        'report_py3o'. Invoice and hs code of each products in this sale order
        would be provided to display in this report with the specific
        format.""",
    "version": "10.0.1.0.0",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": [
        "base_sale_export",
        "report_py3o",
    ],
    "data": [
        "demo/commercial_invoice_report.xml",
    ],
    "installable": True,
}
