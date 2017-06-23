# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestStockPackagingLot(common.TransactionCase):

    def setUp(self):
        super(TestStockPackagingLot, self).setUp()
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
