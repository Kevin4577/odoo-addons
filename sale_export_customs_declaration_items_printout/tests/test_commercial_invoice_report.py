# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError
from odoo.addons.sale_export_customs_declaration_items_printout.models. \
    sale_export_customs_declaration_items_printout import change_ctx


class TestSaleExportCustomsDeclarationItemsPrintout(common.TransactionCase):
    def setUp(self):
        super(TestSaleExportCustomsDeclarationItemsPrintout, self).setUp()
        self.base_sale_export_model = self.env['trading.sale']
        self.stock_picking_model = self.env['stock.picking']
        self.sale_order_model = self.env['sale.order']
        self.product_hs_code_model = self.env['product.hs.code']
        self.partner_id = self.env.ref('base.res_partner_2')
        self.pricelist = self.env.ref('product.list0')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_5 = self.env.ref('product.product_product_5')
        self.ir_actions_report_xml = self.env['ir.actions.report.xml']
        self.report_xml_id = self.env.ref(
            'sale_export_customs_declaration_items_printout.'
            'sale_export_customs_declaration_items_printout_py3o'
        )
        self.tax = self.env['account.tax'].\
            create({'name': 'Expense 10%',
                    'amount': 10,
                    'amount_type': 'percent',
                    'type_tax_use': 'purchase',
                    'price_include': True,
                    })

        self.product_hs_code = self.product_hs_code_model.\
            create({'hs_code': 'TEST HS CODE',
                    'name': 'Test Name',
                    'cn_name': 'CN_NAME',
                    'uom_id': self.product_uom_unit.id,
                    'tax_id': self.tax.id})

        self.product_4.write({'product_hs_code_id': self.product_hs_code.id})
        self.product_5.write({'product_hs_code_id': self.product_hs_code.id})
        self.partner_id.write({'ref': 'test_ref'})
        self.sale_order = self.sale_order_model.create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [(0, 0, {
                'name': self.product_4.name,
                'product_id': self.product_4.id,
                'product_uom_qty': 5.0,
                'product_uom': self.product_uom_unit.id,
                'price_unit': 100.0})]
        })

    def test_render_report(self):
        self.sale_order.action_confirm()
        for pick in self.sale_order.picking_ids:
            pick.force_assign()
            pick.pack_operation_product_ids.qty_done = 3.0
            pick.put_in_pack()
            pick.action_done()
            change_ctx(self.report_xml_id, {'objects': pick, 'data': {}})
        with self.assertRaises(ValidationError):
            for pick in self.sale_order.picking_ids:
                pick.sale_id = False
                change_ctx(self.report_xml_id,
                           {'objects': pick, 'data': {}})
