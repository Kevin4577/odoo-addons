# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProductHSCode(common.TransactionCase):

    def setUp(self):
        super(TestProductHSCode, self).setUp()
        self.prod_hs_code_obj = self.env['product.hs.code']
        self.prod_hs_code = self.prod_hs_code_obj.create({
            'hs_code': 'HSCode1',
            'name': 'Test1',
        })

    def test_check_hs_code(self):
        "Test product code based on sequence"
        with self.assertRaises(ValidationError):
            self.prod_hs_code2 = self.prod_hs_code.create({
                'hs_code': 'HSCode1',
                'name': 'HSCode1',
            })

    def test_copy(self):
        "Test to reset product hs code"
        self.prod_hs_code.copy()
