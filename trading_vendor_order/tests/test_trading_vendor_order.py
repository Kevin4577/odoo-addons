# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from odoo.addons.trading_vendor_contract.report.\
    trading_vendor_contract import render_report_with_data
from odoo.exceptions import ValidationError


class TestTradingVendorOrder(common.TransactionCase):

    def setUp(self):
        super(TestTradingVendorOrder, self).setUp()
        self.report_xml_id = self.env.ref('trading_vendor_contract.'
                                          'trading_vendor_contract_py3o')
        self.supplierinfo_obj = self.env['product.supplierinfo']
        self.PurchaseOrder = self.env['purchase.order']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id_2 = self.env.ref('base.res_partner_2')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.trading_vendor_obj = self.env['trading.vendor']
        seller_vals = {'name': self.partner_id.id, 'min_qty': 1,
                       'price': 500, 'product_code': 'test'}
        (self.product_id_1).write({'purchase_method': 'purchase',
                                   'seller_ids': [(0, 0, seller_vals)]})

        po_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().
                    strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }
        self.po = self.PurchaseOrder.create(po_vals)

        seller_vals_1 = {'name': self.partner_id_2.id, 'min_qty': 1,
                         'price': 500, 'product_code': 'test'}
        (self.product_id_1).write({'purchase_method': 'purchase',
                                   'seller_ids': [(0, 0, seller_vals_1)]})

        po_vals_1 = {
            'partner_id': self.partner_id_2.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().
                    strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }
        self.po_1 = self.PurchaseOrder.create(po_vals_1)
        self.po_list = [self.po + self.po_1]

    def test_render_template_with_data(self):
        with self.assertRaises(ValidationError):
            render_report_with_data(self.report_xml_id,
                                    {'objects': self.po_list[0]})
        render_report_with_data(self.report_xml_id,
                                {'objects': self.po})
