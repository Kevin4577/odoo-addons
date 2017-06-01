# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo.exceptions import ValidationError
from odoo.addons.sale.tests.test_sale_common import TestSale


class TestSaleOrder(TestSale):

    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.product1 = self.env['product.product'].\
            create({'name': 'Test Produdct1',
                    'default_code': False})
        self.partner_id = self.env['res.partner'].\
            create({'name': 'Test Customer',
                    'ref': False})
        vals = {
            'partner_id': self.partner_id.id,
            'order_line': [(0, 0, {'name': self.product1.name,
                                   'product_id': self.product1.id,
                                   'product_uom_qty': 2,
                                   'product_uom': self.product1.uom_id.id,
                                   'price_unit': self.product1.list_price})],
            'pricelist_id': self.env.ref('product.list0').id,
        }
        self.sale = self.env['sale.order'].create(vals)

    def test_action_confirm(self):
        """Check whether customer and product has or not internal reference
        number"""
        with self.assertRaises(ValidationError):
            self.sale.action_confirm()

        self.partner_id.write({'ref': 'test_reference'})
        with self.assertRaises(ValidationError):
            self.sale.action_confirm()

        self.product1.write({'default_code': 'Test Default Code'})
        self.sale.action_confirm()
