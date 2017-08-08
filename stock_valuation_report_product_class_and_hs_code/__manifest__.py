# -*- coding: utf-8 -*-
#   2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Valutaion Report With Product Class and HS code',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    "summary": """Stock Valuation Report With Product Class and HS code""",
    "support": "support@elico-corp.com",
    'depends': [
        'stock_valuation_report',
        'sale_product_hs_code_china',
        'product_class',
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
        'report/report.xml',
        'wizard/wizard_stock_valuation_list.xml',
        'views/stock_valuation.xml'
    ],
    'demo': [
        'demo/hs_code_demo.xml',
    ],
    'installable': True,
    'application': False,
}
