# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestSaleOrder(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.product1 = self.env['product.product'].\
            create({'name': 'Test Produdct1',
                    'default_code': False})
        self.partner_id = self.env['res.partner'].\
            create({'name': 'Test Customer',
                    'ref': False})
        self.partner = self.env.ref('base.res_partner_1')
        vas = {
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {'name': self.product1.name,
                                   'product_id': self.product1.id,
                                   'product_uom_qty': 2,
                                   'product_uom': self.product1.uom_id.id,
                                   'price_unit': self.product1.list_price})],
            'pricelist_id': self.env.ref('product.list0').id,
        }
        self.so = self.env['sale.order'].create(vas)

    def test_action_confirm(self):
        """Check whether customer and product has or not internal reference
        number"""
        with self.assertRaises(ValidationError):
            self.so.action_confirm()
        self.partner.write({'ref': 'test_reference'})
        with self.assertRaises(ValidationError):
            self.so.action_confirm()
