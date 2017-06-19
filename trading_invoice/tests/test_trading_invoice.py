# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from datetime import datetime


class TestTradingInvoice(common.TransactionCase):

    def setUp(self):
        super(TestTradingInvoice, self).setUp()
        self.trading_invoice_model = self.env['trading.invoice']
        self.sale_order_model = self.env['sale.order']
        self.sale_advance_payment_inv_model =\
            self.env['sale.advance.payment.inv']
        self.pack_obj = self.env['stock.quant.package']
        self.Procurementorder = self.env['procurement.order']
        self.product_packaging_model = self.env['product.packaging']
        self.production_lot_model = self.env['stock.production.lot']
        self.pack_operation_model = self.env['stock.pack.operation']
        self.pack_operation_lot_model = self.env['stock.pack.operation.lot']
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write({
            'invoice_policy': 'order',
            'customer_product_code': 'Test'
        })
        self.product_5 = self.env.ref('product.product_product_5')
        self.product_5.write({
            'invoice_policy': 'order',
            'customer_product_code': 'Test'
        })
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner3_id = self.env.ref('base.res_partner_3')
        self.pricelist = self.env.ref('product.list0')
        self.shipping_model = self.env['shipping']
        self.shipping_id = self.shipping_model.create({
            'name': 'Test Shipping',
            'ship_from': self.partner_id.id,
            'ship_to': self.partner3_id.id,
            'ship_by': 'Test Ship By',
        })
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
        self.sale_order.picking_ids.action_confirm()
        self.sale_order.picking_ids[0].write({
            'ship_info_id': self.shipping_id.id
        })
        self.sale_order.picking_ids.action_assign()
        self.sale_order.picking_ids.force_assign()
        self.pack1 = self.pack_obj.create({
            'name': 'Test PACKINOUTTEST'
        })
        self.sale_order.picking_ids.\
            pack_operation_ids[0].result_package_id = self.pack1
        self.sale_order.picking_ids.pack_operation_product_ids.write({
            'qty_done': 5.0
        })
        self.packaging_id = self.product_packaging_model.create({
            'name': 'Test box of 10'
        })
        self.sale_order.picking_ids.pack_operation_product_ids[0].\
            result_package_id.write({
                'packaging_id': self.packaging_id.id
            })
        self.lot1 = self.production_lot_model.create({
            'product_id': self.product_4.id,
            'name': 'Test LOT1',
            'volume': 10.0,
            'carton_qty': 5.0
        })
        pack_opt = self.pack_operation_model.\
            search([('picking_id', '=', self.sale_order.picking_ids[0].id)],
                   limit=1)
        self.pack_operation_lot_model.create({
            'operation_id': pack_opt.id,
            'lot_id': self.lot1.id,
            'qty': 5.0
        })
        self.sale_order.picking_ids.do_new_transfer()
        self.sale_advance_payment_inv_model.with_context({
            'active_id': self.sale_order.id,
            'active_ids': self.sale_order.ids,
            'active_model': 'sale.order',
        }).create({
            'advance_payment_method': 'delivered'
        }).create_invoices()

    def test_get_order_lines(self):
        self.lines = self.trading_invoice_model.\
            get_order_lines(self.sale_order.picking_ids)
        qty = 0.0
        for order in self.sale_order.order_line:
            qty += order.product_uom_qty
        self.assertEqual(self.lines['sum_qty'], qty)
        self.assertEqual(self.lines['sum_amount'],
                         self.sale_order.amount_total)

    def test_get_product_lot_list_per_sale_order(self):
        self.order = self.trading_invoice_model.\
            get_product_lot_list_per_sale_order(self.sale_order.picking_ids)
        self.assertEqual(self.order['location_id'],
                         self.sale_order.picking_ids.location_id)
        self.assertEqual(self.order['sum_carton_qty'], self.lot1.carton_qty)

    def test_get_product_order_list_with_qty(self):
        self.product_order_list = self.trading_invoice_model.\
            get_product_order_list_with_qty(self.sale_order.picking_ids)
        self.assertEqual(self.product_order_list['ship_info_id'],
                         self.shipping_id)
        self.assertEqual(self.product_order_list['partner_shipping_id'],
                         self.sale_order.picking_ids.sale_id.
                         partner_shipping_id)

    def test_get_product_lot_list_per_package_number(self):
        self.product_lot = self.trading_invoice_model.\
            get_product_lot_list_per_package_number(self.
                                                    sale_order.picking_ids)
        self.assertEqual(self.product_lot['ship_to'], self.shipping_id.ship_to)
        self.assertEqual(self.product_lot['print_date'],
                         datetime.today().strftime('%Y-%m-%d'))
        self.assertEqual(self.product_lot['sum_meas'], self.lot1.volume)

    def test_get_order_lines_per_invoice(self):
        self.lines_per_invoice = self.trading_invoice_model.\
            get_order_lines_per_invoice(self.sale_order.invoice_ids)
        self.assertEqual(self.lines_per_invoice['sum_amount'],
                         self.sale_order.amount_total)
        self.assertEqual(self.lines_per_invoice['ship_to'],
                         self.shipping_id.ship_to)

    def test_get_detail_lot_list_per_invoice(self):
        self.detail_lot_list = self.trading_invoice_model.\
            get_detail_lot_list_per_invoice(self.sale_order.invoice_ids)
        self.assertEqual(self.detail_lot_list['total_meas'],
                         self.lot1.volume)
        self.assertEqual(self.detail_lot_list['ship_info_id'],
                         self.shipping_id)
        self.assertEqual(self.detail_lot_list['package_list'][0]['pallet_sum'],
                         self.lot1.carton_qty)

    def test_get_invoice_lines_per_invoice(self):
        self.invoice_lines = self.trading_invoice_model.\
            get_invoice_lines_per_invoice(self.sale_order.invoice_ids)
        self.assertEqual(self.invoice_lines['product_lines'][0]['price_unit'],
                         self.sale_order.order_line[0]['price_unit'])
        self.assertEqual(self.invoice_lines['product_lines'][0]
                         ['price_subtotal'],
                         self.sale_order.
                         order_line[0]['price_unit'] * self.sale_order.
                         order_line[0]['product_uom_qty'])

    def test_get_package_name_per_package_list(self):
        self.package_list = self.trading_invoice_model.\
            get_package_name_per_package_list(self.sale_order.picking_ids)
        self.assertEqual(self.package_list[0]['list'][0], self.pack1.name)
        self.assertEqual(self.package_list[0]['name'], self.packaging_id.name)

    def test_get_pack_lot_list_per_package_type(self):
        self.pack_lot_list = self.trading_invoice_model.\
            get_pack_lot_list_per_package_type(self.sale_order.picking_ids)
        self.assertEqual(self.pack_lot_list['partner_shipping_id'],
                         self.shipping_id.ship_to)
