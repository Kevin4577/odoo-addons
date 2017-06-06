# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestCommercialInvoiceReport(common.TransactionCase):

    def setUp(self):
        super(TestCommercialInvoiceReport, self).setUp()
        self.base_sale_export_model = self.env['base.sale.export']
        self.stock_picking_model = self.env['stock.picking']
        self.sale_order_model = self.env['sale.order']
        self.product_hs_code_model = self.env['product.hs.code']
        self.partner_id = self.env.ref('base.res_partner_2')
        self.pricelist = self.env.ref('product.list0')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_5 = self.env.ref('product.product_product_5')

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
        picking = self.stock_picking_model.\
            search([('sale_id', '=', self.sale_order.id)])
        self.data = {}
        self.data['sum_qty'], self.data['sum_amount'], \
            self.data['product_lines'] =\
            self.base_sale_export_model.get_product_sale_list(picking.sale_id)
        self.data['pallet_sum'], gross_weight, net_weight, volume, \
            package_list = \
            self.base_sale_export_model.get_product_stock_list(picking)

    def test_get_product_sale_list(self):
        self.assertEqual(self.sale_order.amount_total,
                         self.data['sum_amount'])
        self.assertEqual(self.data['product_lines'][0]['qty'],
                         self.data['sum_qty'])
