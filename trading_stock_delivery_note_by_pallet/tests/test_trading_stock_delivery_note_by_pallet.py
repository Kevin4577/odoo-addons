# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.addons.trading_stock_delivery_note_by_pallet.report.\
    trading_stock_delivery_note_by_pallet import render_report_with_data
from odoo.exceptions import ValidationError
from datetime import datetime


class TestTradingStockDeliveryNoteBypallet(common.TransactionCase):

    def setUp(self):
        super(TestTradingStockDeliveryNoteBypallet, self).setUp()
        self.report_xml_id =\
            self.env.ref('trading_stock_delivery_note_by_pallet.'
                         'trading_stock_delivery_note_by_pallet_py3o')
        self.ir_actions_report_xml_model = self.env['ir.actions.report.xml']
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
        })
        self.product_5 = self.env.ref('product.product_product_5')
        self.product_5.write({
            'invoice_policy': 'order',
            'customer_product_code': 'Test',
            'default_code': 'Test Default Code 2',
            'property_account_income_id': self.account_rev_id.id,
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

    def test_render_report_with_invoice(self):
        self.sale_order.picking_ids.write({
            'invoice_id': self.sale_order.invoice_ids[0].id
        })
        render_report_with_data(
            self.report_xml_id,
            {
                'objects': self.sale_order.invoice_ids
            }
        )

    def test_render_report_without_invoice(self):
        with self.assertRaises(ValidationError):
            render_report_with_data(
                self.report_xml_id,
                {
                    'objects': self.sale_order.invoice_ids
                }
            )

    def test_render_report_without_sale_order(self):
        with self.assertRaises(ValidationError):
            for line in self.sale_order.invoice_ids.invoice_line_ids:
                line.sale_line_ids = False
            render_report_with_data(
                self.report_xml_id,
                {
                    'objects': self.sale_order.invoice_ids,
                    'data': {}
                }
            )
