# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trading Vendor Delay Rate Summary',
    'version': '10.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Trading Vendor Delay Rate Summary',
    "support": "support@elico-corp.com",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'trading_vendor',
        'report_py3o',
        'sale'
    ],
    'data': [
        'views/purchase_view.xml',
        'report/trading_vendor_delay_rate_summary.xml',
    ],
    'installable': True,
}
