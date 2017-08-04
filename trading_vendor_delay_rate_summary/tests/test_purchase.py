# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime


class TestPurchaseOrderLine(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrderLine, self).setUp()
        self.PurchaseOrder = self.env['purchase.order']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.SaleOrder = self.env['sale.order']
        self.ProcurementOrder = self.env['procurement.order']
        self.purchase_route_warehouse0_buy_id =\
            self.env.ref('purchase.route_warehouse0_buy').id
        self.route_warehouse0_mto_id =\
            self.env.ref('stock.route_warehouse0_mto').id
        self.partner_18 = self.env.ref('base.res_partner_18')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.partner_18.write({'ref': 'Test Reference'})
        self.partner_id.write({'ref': 'Test Reference 1'})
        self.product_icecream = self.env.ref('stock.product_icecream')
        self.product_icecream.write({'default_code': 'Test Default Code'})
        self.product_uom_kgm = self.env.ref('product.product_uom_kgm')
        seller_vals = {'name': self.partner_id.id, 'min_qty': 1,
                       'price': 500, 'product_code': 'Test'}
        self.product_icecream.write({
            'route_ids': [(6, 0, [self.purchase_route_warehouse0_buy_id,
                                  self.route_warehouse0_mto_id])],
            'seller_ids': [(0, 0, seller_vals)]})
        self.sale_order = self.SaleOrder.create({
            'partner_id': self.partner_18.id,
            'order_line': [(0, 0, {
                'name': 'Ice Cream',
                'product_id': self.product_icecream.id,
                'product_uom_qty': 2,
                'product_uom': self.product_uom_kgm.id,
                'price_unit': 750.00})]
        })
        self.sale_order.action_confirm()
        self.p_order = self.ProcurementOrder.\
            search([('group_id', '=', self.sale_order.name),
                    ('product_id', '=', self.product_icecream.id),
                    ('purchase_id', '!=', False)],
                   limit=1)
        self.p_order.run()

        seller_vals = {'name': self.partner_id.id, 'min_qty': 1,
                       'price': 500, 'product_code': 'test'}
        (self.product_id_1).write({'purchase_method': 'purchase',
                                   'seller_ids': [(0, 0, seller_vals)]})

        self.date_after = datetime.\
            strptime(datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                     DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta(days=1)
        self.date_before = datetime.\
            strptime(datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                     DEFAULT_SERVER_DATETIME_FORMAT) - relativedelta(days=1)

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
        self.po.button_confirm()
        self.po.action_view_picking()
        self.po.order_line[0].move_ids[0].picking_id.do_new_transfer()
        self.env['stock.immediate.transfer'].with_context({
            'active_id': self.po.order_line[0].move_ids[0].picking_id.id,
            'active_ids': self.po.order_line[0].move_ids[0].picking_id.ids,
            'active_model': 'stock.picking',
            }).create({'pick_id':
                       self.po.order_line[0].move_ids[0].picking_id.id
                       }).process()
        self.assertEqual(self.po.order_line[0].move_ids[0].picking_id.state,
                         "done")
        self.line_date = datetime.strptime(
            self.po.order_line[0].date_received,
            DEFAULT_SERVER_DATETIME_FORMAT).date()
        self.picking_date = datetime.strptime(
            self.po.order_line[0].move_ids[0].picking_id.date,
            DEFAULT_SERVER_DATETIME_FORMAT).date()
        self.assertEqual(self.line_date, self.picking_date)

    def test_compute_method(self):
        """Test compute method"""
        for line in self.p_order.purchase_id.order_line:
            line._compute_sale_person()

    def test_compute_is_delayed(self):
        """Test compute_is_delayed method"""
        for po_line in self.po.order_line:
            po_line.date_received = self.date_after
            po_line._compute_is_delayed()

    def test_compute_is_delayed_date(self):
        """Test compute_is_delayed method"""
        for po_line in self.po.order_line:
            po_line.date_received = self.date_before
            po_line._compute_is_delayed()

    def test_compute_year_order(self):
        """Test compute_year_order method"""
        for po_line in self.po.order_line:
            po_line._compute_year_order()
