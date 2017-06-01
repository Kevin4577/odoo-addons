# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestStockProductionLot(common.TransactionCase):

    def setUp(self):
        super(TestStockProductionLot, self).setUp()
        self.stock_production_lot_obj = self.env['stock.production.lot']
        self.product_id = self.env.ref('product.product_product_25').id
        self.stock_production_lot = self.stock_production_lot_obj.create({
            'name': 'Test0001',
            'product_id': self.product_id,
            'qty_per_carton': 5,
            'box_per_carton': 2,
            'gross_by_carton': 2.5,
            'carton_qty': 2,
            'net_by_carton': 1.5,
        })

    def test_compute_qty_per_box(self):
        "Test compute Qty per box"
        self.assertEqual(self.stock_production_lot.qty_per_box,
                         (self.stock_production_lot.qty_per_carton /
                          self.stock_production_lot.box_per_carton))

    def test_compute_gross_weight(self):
        "Test compute Gross weight"
        self.assertEqual(self.stock_production_lot.gross_weight,
                         (self.stock_production_lot.gross_by_carton *
                          self.stock_production_lot.carton_qty))

    def test_compute_net_weight(self):
        "Test compute Net weight"
        self.assertEqual(self.stock_production_lot.net_weight,
                         (self.stock_production_lot.net_by_carton *
                          self.stock_production_lot.carton_qty))
