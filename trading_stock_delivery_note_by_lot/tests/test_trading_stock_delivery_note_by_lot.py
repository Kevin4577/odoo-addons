# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.addons.trading_stock_delivery_note_by_lot.report.\
    trading_stock_delivery_note_by_lot import render_report_with_data
from odoo.exceptions import ValidationError


class TestTradingStockDeliveryNoteByLot(common.TransactionCase):

    def setUp(self):
        super(TestTradingStockDeliveryNoteByLot, self).setUp()
        self.report_xml_id =\
            self.env.ref('trading_stock_delivery_note_by_lot.'
                         'trading_stock_delivery_note_by_lot_py3o')
        self.ir_actions_report_xml_model = self.env['ir.actions.report.xml']
        self.sale_order_model = self.env['sale.order']
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id.write({'ref': 'test_reference'})
        self.partner1_id = self.env.ref('base.res_partner_1')
        self.partner1_id.write({'ref': 'test_reference 1'})
        self.pricelist = self.env.ref('product.list0')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write({ 'default_code': 'Test Default Code 1'})
        self.product_5 = self.env.ref('product.product_product_5')
        self.product_5.write({ 'default_code': 'Test Default Code 2'})
        self.picking_type_out = self.ref('stock.picking_type_out')
        self.location_stock = self.env.ref('stock.stock_location_stock')
        self.loc_customers = self.env.ref('stock.stock_location_customers')

        self.picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_out,
            'location_id': self.location_stock.id,
            'location_dest_id': self.loc_customers.id
        })
        self.picking_1 = self.env['stock.picking'].create({
            'partner_id': self.partner1_id.id,
            'picking_type_id': self.picking_type_out,
            'location_id': self.location_stock.id,
            'location_dest_id': self.loc_customers.id
        })

        self.tax = self.env['account.tax'].\
            create({'name': 'Expense 10%',
                    'amount': 10,
                    'amount_type': 'percent',
                    'type_tax_use': 'purchase',
                    'price_include': True,
                    })

        self.sale_order = self.sale_order_model.\
            create({'partner_id': self.partner_id.id,
                    'pricelist_id': self.pricelist.id,
                    'order_line':
                    [(0, 0, {'name': self.product_4.name,
                             'product_id': self.product_4.id,
                             'product_uom_qty': 5.0,
                             'product_uom': self.product_uom_unit.id,
                             'price_unit': 100.0}),
                     (0, 0, {'name': self.product_5.name,
                             'product_id': self.product_5.id,
                             'product_uom_qty': 4.0,
                             'product_uom': self.product_uom_unit.id,
                             'price_unit': 120.0
                             })
                     ]
                    })
        self.sale_order.action_confirm()

    def test_render_report_with_data(self):
        for picking in self.sale_order.picking_ids:
            render_report_with_data(self.report_xml_id, {'objects': picking})
        with self.assertRaises(ValidationError):
            for picking in self.sale_order.picking_ids:
                picking.sale_id = False
                render_report_with_data(self.report_xml_id,
                                        {'objects': picking})

    def test_check_picking_in_partner(self):
        pickings = self.picking + self.picking_1
        with self.assertRaises(ValidationError):
            render_report_with_data(self.report_xml_id,
                                    {'objects': pickings})
