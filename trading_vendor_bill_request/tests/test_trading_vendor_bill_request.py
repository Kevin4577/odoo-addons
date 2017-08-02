# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from odoo.addons.trading_vendor_bill_request.models.\
    trading_vendor_bill_request import render_report_with_data


class TestTradingVendorBillRequest(common.TransactionCase):

    def setUp(self):
        super(TestTradingVendorBillRequest, self).setUp()
        self.report_xml_id =\
            self.env.ref('trading_vendor_bill_request.'
                         'trading_vendor_bill_request_py3o')
        self.account_invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.tax_model =self.env['account.tax']
        self.account_model = self.env['account.account']
        self.AccountJournal = self.env['account.journal']
        self.account_type_expenses =\
            self.env.ref('account.data_account_type_expenses')
        self.account_type_receivable =\
            self.env.ref('account.data_account_type_receivable')
        self.invoice_line_account = self.account_model.\
            search([('user_type_id', '=', self.account_type_expenses.id)],
                   limit=1).id
        invoice_account = self.account_model.\
            search([('user_type_id', '=', self.account_type_receivable.id)],
                   limit=1).id
        self.partner = self.env.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_4')
        self.tax = self.tax_model.create({
            'name': 'Tax 10.0',
            'amount': 10.0,
            'amount_type': 'fixed',
        })
        self.invoice = self.account_invoice_model.create({
            'partner_id': self.partner.id,
#            'account_id': invoice_account,
        })
        self.invoice_line_model.create({
            'product_id': self.product.id,
            'quantity': 11.0,
            'price_unit': 100.0,
            'invoice_id': self.invoice.id,
            'name': 'product that cost 100',
            'account_id': self.invoice_line_account,
            'invoice_line_tax_ids': [(6, 0, [self.tax.id])],
        })
        self.invoice.action_invoice_open()
        print "\n\n-------self.invoice ----",self.invoice, self.invoice.amount_total
        self.journal = self.AccountJournal.search([('type', '=', 'bank'), ('company_id', '=', self.invoice.company_id.id)], limit=1)
        self.invoice.pay_and_reconcile(self.journal, self.invoice.amount_total)

    def test_report_method(self):
        """Test Report method"""
        render_report_with_data(self.report_xml_id,
                                {'objects': self.invoice})
