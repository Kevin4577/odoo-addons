# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
import odoo
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TestStockValuation(common.TransactionCase):

    def setUp(self):
        super(TestStockValuation, self).setUp()
        self.product_hs_code_id = \
            self.env.ref(
                'stock_valuation_report_product_class_and_hs_code.'
                'product_hs_code_1'
            ).id
        self.stage_id = self.env.ref('product_class.product_stage_data_1').id
        self.class_id = self.env.ref('product_class.product_class_data_1').id
        self.line_id = self.env.ref('product_class.product_line_data_1').id
        self.family_id = self.env.ref('product_class.product_family_data_1').id
        self.order_point_model = self.env['stock.warehouse.orderpoint']
        self.mrp_order1 = self.env.ref('mrp.mrp_production_1')
        self.mrp_order2 = self.env.ref('mrp.mrp_production_2')
        self.report_xml_id =\
            self.env.ref('stock_valuation_report.'
                         'report_stock_valuation')
        self.ir_actions_report_xml_model = self.env['ir.actions.report.xml']
        self.sale_order_model = self.env['sale.order']
        self.stock_valuation_model = self.env['stock.valuation']
        self.stock_valuation_list_model = \
            self.env['wizard.stock.valuation.list']
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id.write({'ref': 'test_reference'})
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner1_id = self.env.ref('base.res_partner_1')
        self.partner1_id.write({'ref': 'test_reference 1'})
        self.pricelist = self.env.ref('product.list0')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write(
            {
                'default_code': 'Test Default Code 1',
                'product_stage_id': self.stage_id,
                'product_line_id': self.line_id,
                'product_class_id': self.class_id,
                'product_family_id': self.family_id,
                'product_hs_code_id': self.product_hs_code_id
            }
        )
        self.product_5 = self.env.ref('product.product_product_5')
        self.product_5.write({'default_code': 'Test Default Code 2'})
        self.picking_type_out = self.ref('stock.picking_type_out')
        self.location_stock = self.env.ref('stock.stock_location_stock')
        self.loc_customers = self.env.ref('stock.stock_location_customers')
        self.partner3_id = self.env.ref('base.res_partner_3')
        self.pack_obj = self.env['stock.quant.package']
        self.product_packaging_model = self.env['product.packaging']
        self.production_lot_model = self.env['stock.production.lot']
        self.pack_operation_model = self.env['stock.pack.operation']
        self.pack_operation_lot_model = self.env['stock.pack.operation.lot']
        self.picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_out,
            'location_id': self.location_stock.id,
            'location_dest_id': self.loc_customers.id
        })
        self.OrderPoint4 = self.order_point_model.create({
            'product_id': self.product_4.id,
            'product_max_qty': 0.0,
            'product_min_qty': 10.0
        })
        self.stock_valuation = self.stock_valuation_model.create(
            {
                'name': 'Test_Reference',
            }
        )
        self.po_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().strftime(
                        DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }
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
        self.sale_order.picking_ids.action_confirm()
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
            result_package_id.write({'packaging_id': self.packaging_id.id})
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

    def test_10_render_report_with_product_class(self):
        self.stock_valuation._selection_filter_by_product_class()
        self.stock_valuation._selection_filter_by_hs_code()
        self.stock_valuation.onchange_filter_by_product_class()
        self.stock_valuation.onchange_filter_by_hs_code()
        self.stock_valuation.write({
            'product_stage_id': self.stage_id,
            'product_line_id': self.line_id,
            'product_class_id': self.class_id,
            'product_family_id': self.family_id
        })
        context = self.stock_valuation.prepare_valuation()
        context['context'].update(uid=self.uid)
        self.stock_valuation_list = \
            self.stock_valuation_list_model.with_context(
                context['context']
            ).create({
                'location_id': self.stock_valuation.location_id.id,
            })
        datas = self.stock_valuation_list.xlsx_export()
        self.dataB = datas['datas']
        self.new_dict = {}
        for (key, item) in self.dataB['title'].items():
            self.new_dict[str(key)] = item
        self.dataB['title'] = self.new_dict
        self.stock_valuation_report = odoo.report.render_report(
            self.cr,
            self.uid,
            self.stock_valuation_list.id,
            'stock.valuation.report.xlsx.product.class.hs.code',
            self.dataB,
        )

    def test_20_render_report_with_product_category(self):
        self.stock_valuation.write({
            'product_hs_code_id': self.product_hs_code_id,
        })
        context = self.stock_valuation.prepare_valuation()
        context['context'].update(uid=self.uid)
        self.stock_valuation_list = \
            self.stock_valuation_list_model.with_context(
                context['context']
            ).create({
                'location_id': self.stock_valuation.location_id.id,
            })
