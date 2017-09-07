# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from datetime import datetime


class TestTradingSale(common.TransactionCase):

    def setUp(self):
        super(TestTradingSale, self).setUp()
        self.trading_sale = self.env['trading.sale']
        self.sale_order_model = self.env['sale.order']
        IrModelData = self.env['ir.model.data']
        self.account_obj = self.env['account.account']
        self.advance_product = self.env.ref('sale.advance_product_0')
        self.sale_advance_payment_inv_model = \
            self.env['sale.advance.payment.inv']
        self.pack_obj = self.env['stock.quant.package']
        self.Procurementorder = self.env['procurement.order']
        self.product_packaging_model = self.env['product.packaging']
        self.production_lot_model = self.env['stock.production.lot']
        self.pack_operation_model = self.env['stock.pack.operation']
        self.pack_operation_lot_model = self.env['stock.pack.operation.lot']
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.prod_hs_code_obj = self.env['product.hs.code']
        self.prod_hs_code1 = self.prod_hs_code_obj.create({
            'hs_code': 'HSCode1',
            'name': 'Test1',
        })
        self.prod_hs_code2 = self.prod_hs_code_obj.create({
            'hs_code': 'HSCode2',
            'name': 'Test2',
        })
        user_type_id = IrModelData.xmlid_to_res_id(
            'account.data_account_type_revenue')
        self.account_rev_id = self.account_obj.create(
            {'code': 'X2020', 'name': 'Sales - Test Sales Account',
             'user_type_id': user_type_id, 'reconcile': True})
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write({
            'invoice_policy': 'order',
            'customer_product_code': 'Test',
            'default_code': 'Test Default Code',
            'property_account_income_id': self.account_rev_id.id,
            'product_hs_code_id': self.prod_hs_code1.id,
        })
        self.product_5 = self.env.ref('product.product_product_5')
        self.product_5.write({
            'invoice_policy': 'order',
            'customer_product_code': 'Test',
            'default_code': 'Test Default Code 2',
            'property_account_income_id': self.account_rev_id.id,
            'product_hs_code_id': self.prod_hs_code2.id
        })
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id.write({'ref': 'test_reference'})
        self.partner3_id = self.env.ref('base.res_partner_3')
        self.pricelist = self.env.ref('product.list0')
        self.shipping_model = self.env['shipping']
        self.shipping_id = self.shipping_model.create({
            'name': 'Test Shipping',
            'ship_from': self.partner_id.id,
            'ship_to': self.partner3_id.id,
            'ship_by': 'Test Ship By',
        })
        self.env['account.journal'].create(
            {
                'name': 'Test',
                'type': 'sale',
                'code': 'BNK11',
                'company_id': self.env.user.company_id.id
            }
        )
        self.env['account.journal'].create(
            {
                'name': 'Test',
                'type': 'sale',
                'code': 'BNK12',
                'company_id': self.partner_id.company_id.id
            }
        )
        self.sale_order = self.sale_order_model.create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.pricelist.id,
            'confirmation_date': datetime.today().strftime('%Y-%m-%d'),
            'order_line': [(0, 0, {'name': self.product_4.name,
                                   'product_id': self.product_4.id,
                                   'product_uom_qty': 5.0,
                                   'product_uom': self.product_uom_unit.id,
                                   'price_unit': 100.0
                                   }),
                           (0, 0, {'name': self.product_5.name,
                                   'product_id': self.product_5.id,
                                   'product_uom_qty': 4.0,
                                   'product_uom': self.product_uom_unit.id,
                                   'price_unit': 120.0
                                   })]
        })
        self.sale_order.action_confirm()
        self.advance_product.write(
            {'property_account_income_id': self.account_rev_id.id, }
        )
        self.sale_order.picking_ids.action_confirm()
        self.sale_order.picking_ids[0].write({
            'ship_info_id': self.shipping_id.id
        })
        self.sale_order.picking_ids.action_assign()
        self.sale_order.picking_ids.force_assign()
        self.pack1 = self.pack_obj.create({
            'name': 'Test PACKINOUTTEST'
        })
        self.sale_order.picking_ids. \
            pack_operation_ids[0].result_package_id = self.pack1
        self.sale_order.picking_ids.pack_operation_product_ids.write({
            'qty_done': 5.0
        })
        self.packaging_id = self.product_packaging_model.create({
            'name': 'Test box of 10'
        })
        self.sale_order.picking_ids.pack_operation_product_ids[0]. \
            result_package_id.write({
                'packaging_id': self.packaging_id.id
            })
        self.lot1 = self.production_lot_model.create({
            'product_id': self.product_4.id,
            'name': 'Test LOT1',
            'volume': 10.0,
            'carton_qty': 5.0
        })
        pack_opt = self.pack_operation_model. \
            search([('picking_id', '=', self.sale_order.picking_ids[0].id)],
                   limit=1)
        self.pack_operation_lot_model.create({
            'operation_id': pack_opt.id,
            'lot_id': self.lot1.id,
            'qty': 5.0,
            'volume': 10.0,
            'carton_qty': 5.0,
        })
        self.sale_order.picking_ids.do_new_transfer()
        self.sale_advance_payment_inv_model.with_context({
            'active_id': self.sale_order.id,
            'active_ids': self.sale_order.ids,
            'active_model': 'sale.order',
        }).create({
            'advance_payment_method': 'delivered',
            'product_id': self.advance_product.id,
        }).create_invoices()
        self.sale_order.picking_ids.write({
            'invoice_id': self.sale_order.invoice_ids[0].id
        })

    def test_get_supplier(self):
        self.trading_sale.get_supplier(self.env.user.company_id)

    def test_get_product_hs_code_list(self):
        """This function should check the filter reporting element of hs
        code for each order lines."""
        self.trading_sale.get_product_hs_code_list(self.sale_order)
        self.sale_order.action_cancel()
        self.sale_order.order_line[0].product_id.product_hs_code_id = False
        self.sale_order.action_confirm()
        self.trading_sale.get_product_hs_code_list(self.sale_order)

    def test_get_product_sale_list_with_pricelist(self):
        """This function should check the filter order lines of
        sale order group by the same hs code of products inside those line.
        Quantity and price total of lines per hs code would be summed.
        Unit price = summary of price total / summary of quantity"""
        self.trading_sale.get_product_sale_list_with_pricelist(
            self.sale_order.invoice_ids
        )
        self.sale_order.order_line[0].product_id.product_hs_code_id = False
        self.trading_sale.get_product_sale_list_with_pricelist(
            self.sale_order.invoice_ids
        )

    def test_get_product_sale_list(self):
        """This function should check the filter order lines of
        sale order group by the same hs code of products inside those line.
        Quantity and price total of lines per hs code would be summed """
        self.trading_sale.get_product_sale_list(self.sale_order.invoice_ids)
        self.sale_order.order_line[0].product_id.product_hs_code_id = False
        self.trading_sale.get_product_sale_list(self.sale_order.invoice_ids)

    def test_get_product_purchase_list(self):
        """This function should check the filter order lines of
        sale order group by the same hs code of products inside those line.
        Quantity and price total of lines per hs code would be summed """
        self.trading_sale.get_product_purchase_list(
            self.sale_order.picking_ids)
        self.sale_order.order_line[0].product_id.product_hs_code_id = False
        self.trading_sale.get_product_purchase_list(
            self.sale_order.picking_ids)

    def test_get_product_stock_list(self):
        """This function should check the filter operation
        lines of stock picking group by the same hs code of products
        inside those line.Carton quantity, total gross weight and total net
        weight of lots of those lines per hs code would be summed."""
        self.trading_sale.get_product_stock_list(self.sale_order.invoice_ids)
        self.sale_order.order_line[0].product_id.product_hs_code_id = False
        self.trading_sale.get_product_stock_list(self.sale_order.invoice_ids)

    def test_get_package_sum(self):
        """This function should check the return the sum of
        quantity, gross weight, and volume of packages which was used in
        this stock picking."""
        self.trading_sale.get_package_sum(self.sale_order.invoice_ids)

    def test_get_date_invoice(self):
        """This function should check the return the sum of
        quantity, gross weight, and volume of packages which was used in
        this stock picking."""
        self.trading_sale.get_date_invoice(self.sale_order.invoice_ids)
