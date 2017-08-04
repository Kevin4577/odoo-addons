# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProductHSCode(common.TransactionCase):

    def setUp(self):
        super(TestProductHSCode, self).setUp()
        product_product = self.env['product.product']
        self.prod_hs_code_obj = self.env['product.hs.code']
        self.prod_hs_code = self.prod_hs_code_obj.create({
            'hs_code': 'HSCode1',
            'name': 'Test1',
        })
        self.product1 = product_product.create({
            'name': 'Test Product',
            'default_code': 'Test Default Code',
            'product_hs_code_id': self.prod_hs_code.id
        })

    def test_check_hs_code(self):
        "Test product code based on sequence"
        with self.assertRaises(ValidationError):
            self.prod_hs_code2 = self.prod_hs_code.create({
                'hs_code': 'HSCode1',
                'name': 'HSCode1',
            })

    def test_product_onchange(self):
        "Test product onchange function"
        self.product1.product_tmpl_id._onchange_product_hs_code_id()
