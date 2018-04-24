# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestSale(common.TransactionCase):

    def setUp(self):
        super(TestSale, self).setUp()
        self.partner_id = self.env.ref('base.res_partner_2')
        self.partner_id.write({'ref': 'test_reference'})
        self.pricelist = self.env.ref('product.list0')
        self.sale_order_model = self.env['sale.order']
        IrModelData = self.env['ir.model.data']
        self.account_obj = self.env['account.account']
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_4 = self.env.ref('product.product_product_4')
        self.product_4.write({'default_code': 'Test Default Code'})
        self.product_stage = self.env.ref('product_class.product_stage_data_1')
        self.product_line = self.env.ref('product_class.product_line_data_1')
        self.product_class = self.env.ref('product_class.product_class_data_1')
        self.product_family = self.env.ref('product_class.'
                                           'product_family_data_1')
        user_type_id = IrModelData.xmlid_to_res_id(
            'account.data_account_type_revenue')
        self.account_rev_id = self.account_obj.create(
            {'code': 'X2020', 'name': 'Sales - Test Sales Account',
             'user_type_id': user_type_id, 'reconcile': True})

        self.product_4.write({'product_stage_id': self.product_stage.id,
                              'product_line_id': self.product_line.id,
                              'product_class_id': self.product_class.id,
                              'product_family_id': self.product_family.id,
                              'property_account_income_id':
                                  self.account_rev_id.id})
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
        self.sale_order = self.sale_order_model.\
            create({'partner_id': self.partner_id.id,
                    'pricelist_id': self.pricelist.id,
                    'order_line':
                    [(0, 0, {'name': self.product_4.name,
                             'product_id': self.product_4.id,
                             'product_uom_qty': 5.0,
                             'product_uom': self.product_uom_unit.id,
                             'price_unit': 100.0,
                             'qty_delivered': 10,
                             'discount': 10.0,
                             'qty_to_invoice': 20,
                             'qty_invoiced': 15})
                     ]
                    })
        self.sale_order.action_confirm()
        self.sale_order.action_invoice_create()

    def test_price_payment(self):
        for order_line in self.sale_order.order_line:
            self.assertEqual(bool(order_line.price_payment), True)