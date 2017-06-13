# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo.tests import common


class TestStockPicking(common.TransactionCase):

    def setUp(self):
        super(TestStockPicking, self).setUp()
        self.PickingObj = self.env['stock.picking']
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.picking_type_out = self.env.ref('stock.picking_type_out')
        self.supplier_location = self.env.ref('stock.stock_location_suppliers')
        self.stock_location = self.env.ref('stock.stock_location_stock')
        self.partner_id = self.env.ref('base.res_partner_4')
        self.picking_in = self._create_picking(
            self.partner_id,
            self.picking_type_in,
            self.supplier_location,
            self.stock_location
        )

    def test_compute_user_group(self):
        self.picking_in.compute_user_group()

    def _create_picking(self, partner, picking_type_in, supplier_location,
                        stock_location):
        picking = self.PickingObj.create({
            'partner_id': partner and partner.id,
            'picking_type_id': picking_type_in and picking_type_in.id,
            'location_id': supplier_location and supplier_location.id,
            'location_dest_id': stock_location and stock_location.id
        })
        return picking
