# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestProductHSCodeChina(common.TransactionCase):

    def setUp(self):
        super(TestProductHSCodeChina, self).setUp()
        self.prod_temp_obj = self.env['product.template']
        self.view_id = self.env.ref('product.'
                                    'product_template_only_form_view').id
        

    def test_fields_view_get(self):
        """Test fields view get method for invisible hs name"""
        self.prod_temp_obj.fields_view_get(view_id=self.view_id)
