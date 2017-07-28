# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class TradingVendor(common.TransactionCase):

    def setUp(self):
        super(TradingVendor, self).setUp()
        self.supplierinfo_obj = self.env['product.supplierinfo']
        self.PurchaseOrder = self.env['purchase.order']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.partner_id_2 = self.env.ref('base.res_partner_2')
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
        self.po_1 = self.PurchaseOrder.create(po_vals_1)
        self.po_list = [self.po, self.po_1]

    def test_get_partner_contact(self):
        """Test Partner Contact method"""
        self.trading_vendor_obj.get_partner_contact(self.partner_id)

    def test_get_purchase_order_vendor_contact(self):
        """Test purchase order vendor contact method"""
        self.trading_vendor_obj.get_purchase_order_vendor_contact(self.po)

    def test_get_purchase_order_company_contact(self):
        """Test purchase order company contact method"""
        self.trading_vendor_obj.get_purchase_order_company_contact(self.po)

    def test_get_purchase_order_total_quantity_and_price(self):
        """Test purchase order total quantity and price method"""
        self.trading_vendor_obj.\
            get_purchase_order_total_quantity_and_price(self.po)

    def test_get_purchase_order_list_total_quantity_and_price(self):
        """Test purchase order list total quantity and price method"""
        self.trading_vendor_obj.\
            get_purchase_order_list_total_quantity_and_price(self.po_list)
