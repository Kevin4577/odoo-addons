# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.trading_invoice_proforma_invoice.models.\
    trading_invoice_proforma_invoice import render_template_with_data
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestTradingInvoiceProformaInvoice(common.TransactionCase):

    def setUp(self):
        super(TestTradingInvoiceProformaInvoice, self).setUp()
        self.report_xml_id = self.env.ref('trading_invoice_proforma_invoice.'
                                          'trading_invoice_proforma_'
                                          'invoice_py3o')
        self.sale_order_model = self.env['sale.order']
        IrModelData = self.env['ir.model.data']
        self.account_obj = self.env['account.account']
        self.advance_product = self.env.ref('sale.advance_product_0')
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id.write({'ref': 'test_reference'})
        self.pricelist = self.env.ref('product.list0')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        user_type_id = IrModelData.xmlid_to_res_id(
            'account.data_account_type_revenue')
        self.account_rev_id = self.account_obj.create(
            {'code': 'X2020', 'name': 'Sales - Test Sales Account',
             'user_type_id': user_type_id, 'reconcile': True})
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write(
            {
                'default_code': 'Test Default Code',
                'property_account_income_id': self.account_rev_id.id,
            }
        )
        self.ir_actions_report_xml = self.env['ir.actions.report.xml']
        self.sale_advance_payment_inv_model =\
            self.env['sale.advance.payment.inv']

        self.tax = self.env['account.tax'].\
            create({'name': 'Expense 10%',
                    'amount': 10,
                    'amount_type': 'percent',
                    'type_tax_use': 'purchase',
                    'price_include': True,
                    })
        self.partner_id.write(
            {
                'property_account_receivable_id': self.account_rev_id.id,
                'property_account_payable_id': self.account_rev_id.id
            }
        )
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
        context = {"active_model": 'sale.order',
                   "active_ids": self.sale_order.ids,
                   "active_id": self.sale_order.id}
        self.sale_order.with_context(context).action_confirm()
        self.advance_product.write(
            {'property_account_income_id': self.account_rev_id.id, }
        )
        payment = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'fixed',
            'amount': 5,
            'product_id': self.advance_product.id,
        })
        self.env['account.journal'].create(
            {
                'name': 'Test',
                'type': 'sale',
                'code': 'BNK11',
                'company_id': self.env.user.company_id.id
            }
        )
        payment.with_context(context).create_invoices()

    def test_render_template_with_data(self):
        "To Test render_template_with_data method."
        render_template_with_data(
            self.report_xml_id, {
                'objects': self.sale_order,
                'company': self.env.user.company_id})
        with self.assertRaises(ValidationError):
            sale_order = self.sale_order.order_line
            sale_order.order_line = False
            render_template_with_data(self.report_xml_id,
                                      {'objects': sale_order,
                                       'company': self.env.user.company_id})
