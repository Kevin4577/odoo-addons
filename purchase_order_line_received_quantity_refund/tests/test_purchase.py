# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class TestPurchase(common.TransactionCase):

    def setUp(self):
        super(TestPurchase, self).setUp()
        self.supplierinfo_obj = self.env['product.supplierinfo']
        self.PurchaseOrder = self.env['purchase.order']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.partner_id_2 = self.env.ref('base.res_partner_2')
        (self.product_id_1).write({'purchase_method': 'purchase',
                                   'seller_ids': [(0, 0,
                                                   {'name': self.partner_id.id,
                                                    'min_qty': 1,
                                                    'price': 500,
                                                    'product_code': 'test'})]})

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

    def test_picking_transfer(self):
        self.po.button_confirm()
        self.picking = self.po.picking_ids[0]
        self.picking.force_assign()
        self.picking.pack_operation_product_ids.write({'qty_done': 5.0})
        self.picking.do_new_transfer()
        # Create return picking
        StockReturnPicking = self.env['stock.return.picking']
        default_data = StockReturnPicking.with_context(
            active_ids=self.picking.ids,
            active_id=self.picking.ids[0]).default_get(
            [
                'move_dest_exists',
                'original_location_id',
                'product_return_moves',
                'parent_location_id',
                'location_id'
            ])
        return_wiz = StockReturnPicking.\
            with_context(active_ids=self.picking.ids,
                         active_id=self.picking.ids[0]).create(default_data)
        return_wiz.product_return_moves.quantity = 2.0
        res = return_wiz.create_returns()
        return_pick = self.env['stock.picking'].browse(res['res_id'])
        # Validate picking
        return_pick.force_assign()
        return_pick.pack_operation_product_ids.write({'qty_done': 2})
        return_pick.do_new_transfer()
