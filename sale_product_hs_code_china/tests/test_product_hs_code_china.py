# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProductHSCodeChina(common.TransactionCase):

    def setUp(self):
        super(TestProductHSCodeChina, self).setUp()
        self.prod_hs_code_obj = self.env['product.hs.code']
        self.prod_hs_code = self.prod_hs_code_obj.create({
            'hs_code': 'HSCode1',
            'name': 'Test1',
        })
        self.prod_temp_obj = self.env['product.template']
        self.hs_manager = self.env.ref('sale_product_hs_code.'
                                       'group_hs_code_manager')
        self.user = self.env.ref('base.user_root')
        self.user.write({'groups_id': [(6, 0, self.hs_manager.ids)]})
        self.view_id = self.env.ref('product.'
                                    'product_template_only_form_view').id
        self.tree_view_id = self.env.ref('product.'
                                         'product_template_tree_view').id

    def test_check_hs_code(self):
        "Test product code based on sequence"
        with self.assertRaises(ValidationError):
            self.prod_hs_code2 = self.prod_hs_code.create({
                'hs_code': 'HSCode1',
                'name': 'HSCode1',
            })

    def test_fields_view_get(self):
        """Test fields view get method for invisible hs name"""
        self.prod_temp_obj.fields_view_get(view_id=self.tree_view_id,
                                           view_type='tree')
        self.prod_temp_obj.fields_view_get(view_id=self.view_id)
