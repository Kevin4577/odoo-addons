# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TradingVendor(common.TransactionCase):

    def setUp(self):
        super(TradingVendor, self).setUp()
        self.SaleOrder = self.env['sale.order']
        self.ProcurementOrder = self.env['procurement.order']
        self.purchase_route_warehouse0_buy_id =\
            self.env.ref('purchase.route_warehouse0_buy').id
        self.route_warehouse0_mto_id =\
            self.env.ref('stock.route_warehouse0_mto').id
        self.partner_18 = self.env.ref('base.res_partner_18')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.product_icecream = self.env.ref('stock.product_icecream')
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

    def test_compute_method(self):
        """Test compute method"""
        qty = 0.0
        for line in self.p_order.purchase_id.order_line:
            qty += line.qty_delivered
            line._compute_price_subtotal_company()
        self.assertEqual(line.qty_delivered,
                         self.sale_order.order_line.product_uom_qty)
