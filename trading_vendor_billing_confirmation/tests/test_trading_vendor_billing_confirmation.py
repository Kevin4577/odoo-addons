# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestTradingVendorBillingConfirmation(common.TransactionCase):

    def setUp(self):
        super(TestTradingVendorBillingConfirmation, self).setUp()
        self.SaleOrder = self.env['sale.order']
        self.account_invoice = self.env['account.invoice']
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

    def test_compute_method(self):
        """Test Compute method"""
        self.account_model = self.env['account.account']
        IrModelData = self.env['ir.model.data']
        user_type_id = IrModelData.xmlid_to_res_id(
            'account.data_account_type_revenue')
        self.account_rev_id = self.account_model.create(
            {'code': 'X2020', 'name': 'Sales - Test Sales Account',
             'user_type_id': user_type_id, 'reconcile': True})
        self.partner_id.write(
            {
                'property_account_receivable_id': self.account_rev_id.id,
                'property_account_payable_id': self.account_rev_id.id
            }
        )
        self.invoice = self.account_invoice.create({
            'partner_id': self.partner_id.id,
            'purchase_id': self.p_order.purchase_id.id,
            'account_id': self.partner_id.property_account_payable_id.id,
            'type': 'in_invoice',
        })
        self.invoice.purchase_order_change()
        self.assertEqual(self.invoice.invoice_line_ids[3].state_sale,
                         self.invoice.invoice_line_ids[3].purchase_line_id.
                         procurement_ids.move_dest_id.state)
