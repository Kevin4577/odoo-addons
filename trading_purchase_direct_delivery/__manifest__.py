# -*- coding: utf-8 -*-
# © 2018 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Trading Purchase Direct Delivery",
    "summary": """This module generates Trading Direct Delivery Note  
     for direct-delivery orders""",
    "version": "10.0.1.0.0",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "depends": [
        "trading_invoice",
        "report_py3o",
    ],
    "data": [
        "report/trading_purchase_direct_delivery.xml",
    ],
    "installable": True,
}
