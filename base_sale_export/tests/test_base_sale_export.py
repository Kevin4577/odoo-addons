# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestBaseSaleExport(common.TransactionCase):

    def setUp(self):
        super(TestBaseSaleExport, self).setUp()
        product_hs_code = self.env['product.hs.code']
        product_product = self.env['product.product']
        self.product_uom = self.env.ref('product.product_uom_unit')
        self.partner = self.env.ref('base.res_partner_1')
        self.base_export = self.env['base.sale.export']
        self.product_hs = product_hs_code.create({
            'hs_code': 'Test HS Code',
            'name': 'Test name',
            'uom_id': self.product_uom.id,
            'description': 'Test Description',
            'note': 'note'
        })
        self.product1 = product_product.create({
            'name': 'Test Product',
            'product_hs_code_id': self.product_hs.id
        })
        self.so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'pricelist_id': self.env.ref('product.list0').id,
            'order_line': [(0, 0, {
                'name': self.product1.name,
                'product_id': self.product1.id,
                'product_uom_qty': 2,
                'product_uom': self.product1.uom_id.id,
                'price_unit': self.product1.list_price,
            })],
        })

    def test_get_product_hs_code_list(self):
        """This function should check the filter reporting element of hs
        code for each order lines."""
        self.so.action_confirm()
        self.base_export.get_product_hs_code_list(self.so)
        self.so.action_cancel()
        self.so.order_line.product_id.product_hs_code_id = False
        self.so.action_confirm()
        self.base_export.get_product_hs_code_list(self.so)

    def test_get_product_sale_list_with_pricelist(self):
        """This function should check the filter order lines of
        sale order group by the same hs code of products inside those line.
        Quantity and price total of lines per hs code would be summed.
        Unit price = summary of price total / summary of quantity"""
        self.so.action_confirm()
        self.base_export.get_product_sale_list_with_pricelist(self.so)
        self.so.order_line.product_id.product_hs_code_id = False
        self.so.action_confirm()
        self.base_export.get_product_sale_list_with_pricelist(self.so)

    def test_get_product_sale_list(self):
        """This function should check the filter order lines of
        sale order group by the same hs code of products inside those line.
        Quantity and price total of lines per hs code would be summed """
        self.so.action_confirm()
        self.base_export.get_product_sale_list(self.so)
        self.so.order_line.product_id.product_hs_code_id = False
        self.so.action_confirm()
        self.base_export.get_product_sale_list(self.so)

    def test_get_product_stock_list(self):
        """This function should check the filter operation
        lines of stock picking group by the same hs code of products
        inside those line.Carton quantity, total gross weight and total net
        weight of lots of those lines per hs code would be summed."""
        self.so.action_confirm()
        self.base_export.get_product_stock_list(self.so.picking_ids)
        self.so.order_line.product_id.product_hs_code_id = False
        self.so.action_confirm()
        self.base_export.get_product_stock_list(self.so.picking_ids)

    def test_get_package_sum(self):
        """This function should check the return the sum of
        quantity, gross weight, and volume of packages which was used in
        this stock picking."""
        self.base_export.get_package_sum(self.so.picking_ids)
        self.so.action_confirm()
        for picking in self.so.picking_ids:
            picking.pack_operation_product_ids.qty_done = 3.0
            # Put in a pack
            picking.put_in_pack()
            self.base_export.get_package_sum(picking)
