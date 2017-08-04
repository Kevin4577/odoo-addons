# -*- coding: utf-8 -*-
#   2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Valutaion',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    "summary": """Stock Valuation Report""",
    "support": "support@elico-corp.com",
    'depends': [
        'mrp',
        'purchase',
        'report_xlsx',
        'stock_account',
    ],
    'external_dependencies': {
        'python': [
            'xlsxwriter',
        ],
    },
    'author': 'Elico Corp',
    'license': 'AGPL-3',
    'website': 'https://www.elico-corp.com',
    'data': [
        'security/stock_valuation_report_security.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        'wizard/wizard_stock_valuation_list.xml',
        'views/stock_valuation.xml'
    ],
    'installable': True,
    'application': False,
}
