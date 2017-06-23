# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.stock.tests.common import TestStockCommon


class TestStockPackagingLot(TestStockCommon):

    def setUp(self):
        super(TestStockPackagingLot, self).setUp()
        self.stock_production_lot_obj = self.env['stock.production.lot']
        self.pack_operation_lot_obj = self.env['stock.pack.operation.lot']
        self.product_id = self.env.ref('product.product_product_25').id
        self.stock_production_lot = self.stock_production_lot_obj.create({
            'name': 'Test0001',
            'product_id': self.productA.id,
            'qty_per_carton': 5,
            'box_per_carton': 2,
            'gross_by_carton': 2.5,
            'carton_qty': 2,
            'net_by_carton': 1.5,
        })

        picking_out = self.PickingObj.create({
            'partner_id': self.partner_delta_id,
            'name': 'testpicking',
            'picking_type_id': self.picking_type_out,
            'location_id': self.stock_location,
            'location_dest_id': self.customer_location})
        self.MoveObj.create({
            'name': self.productA.name,
            'product_id': self.productA.id,
            'product_uom_qty': 1,
            'product_uom': self.productA.uom_id.id,
            'picking_id': picking_out.id,
            'location_id': self.stock_location,
            'location_dest_id': self.customer_location})

        pack = self.StockPackObj.create({
                'product_id': self.productA.id,
                'product_qty': 1,
                'product_uom_id': self.productA.uom_id.id,
                'location_id': self.supplier_location,
                'location_dest_id': self.stock_location,
                'picking_id': picking_out.id})
        self.pack_operation_lot = self.pack_operation_lot_obj.\
            create({'operation_id': pack.id,
                    'lot_id': self.stock_production_lot.id,
                    'qty': 1.0})
        picking_out.action_confirm()
        picking_out.action_assign()
        picking_out.do_transfer()

    def test_onchange_gross_by_carton(self):
        "To Test Gross weight"
        self.stock_production_lot.onchange_gross_by_carton()

    def test_onchange_net_by_carton(self):
        "To Test Net weight"
        self.stock_production_lot.onchange_net_by_carton()

    def test_onchange_qty_per_carton(self):
        "To Test Qty per box"
        self.stock_production_lot.onchange_qty_per_carton()

    def test_onchange_volume_by_carton(self):
        "To Test Qty per box"
        self.stock_production_lot.onchange_volume_by_carton()

    def test_lot_onchange_qty_per_carton(self):
        "To Test Qty per box"
        self.pack_operation_lot.onchange_qty_per_carton()

    def test_lot_onchange_gross_by_carton(self):
        "To Test Gross weight"
        self.pack_operation_lot.onchange_gross_by_carton()

    def test_lot_onchange_net_by_carton(self):
        "To Test Net weight"
        self.pack_operation_lot.onchange_net_by_carton()

    def test_lot_onchange_volume_by_carton(self):
        "To Test Qty per box"
        self.pack_operation_lot.onchange_volume_by_carton()

    def test_lot_onchange_qty_per_carton_carton_qty(self):
        "To Test Qty"
        self.pack_operation_lot.onchange_qty_per_carton_carton_qty()

    def test_lot_onchange_lot_id(self):
        """To select the available lot to input the
        additional lot information into operation lines"""
        self.pack_operation_lot.onchange_lot_id()
