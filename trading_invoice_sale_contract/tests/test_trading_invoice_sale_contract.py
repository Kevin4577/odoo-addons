# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.trading_invoice_sale_contract.models.\
    trading_invoice_sale_contract import render_template_with_data
from odoo.tests import common


class TestTradingInvoiceSaleContract(common.TransactionCase):

    def setUp(self):
        super(TestTradingInvoiceSaleContract, self).setUp()
        self.report_xml_id = self.env.ref('trading_invoice_sale_contract.'
                                          'trading_invoice_sale_contract_py3o')
        self.sale_order_model = self.env['sale.order']
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id.write({'ref': 'test_reference'})
        self.pricelist = self.env.ref('product.list0')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write({'default_code': 'Test Default Code'})
        self.ir_actions_report_xml = self.env['ir.actions.report.xml']

        self.tax = self.env['account.tax'].\
            create({'name': 'Expense 10%',
                    'amount': 10,
                    'amount_type': 'percent',
                    'type_tax_use': 'purchase',
                    'price_include': True,
                    })

        self.sale_order = self.sale_order_model.\
            create({'partner_id': self.partner_id.id,
                    'pricelist_id': self.pricelist.id,
                    'order_line':
                    [(0, 0, {'name': self.product_4.name,
                             'product_id': self.product_4.id,
                             'product_uom_qty': 5.0,
                             'product_uom': self.product_uom_unit.id,
                             'price_unit': 100.0})
                     ]
                    })
        self.sale_order.action_confirm()

    def test_render_template_with_data(self):
        "To Test render_template_with_data method."
        render_template_with_data(
            self.report_xml_id, {
                'objects': self.sale_order})
