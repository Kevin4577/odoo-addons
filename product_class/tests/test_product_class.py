# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProductClass(common.TransactionCase):

    def setUp(self):
        super(TestProductClass, self).setUp()
        self.prod_tmpl_obj = self.env['product.template']
        self.product_tmpl = self.env.ref(
            'product_class.product_template_data_1'
        ).copy({'default_code': ''})
        self.product_tmpl2 = self.product_tmpl.copy({
            'name': 'Test2',
            'default_code': '',
            'product_stage_id': False,
        })
        self.product_tmpl3 = self.product_tmpl.copy({
            'name': 'Test3',
            'default_code': '',
            'product_line_id': False,
        })
        self.product_tmpl4 = self.product_tmpl.copy({
            'name': 'Test4',
            'default_code': '',
            'product_class_id': False,
        })
        self.product_tmpl5 = self.product_tmpl.copy({
            'name': 'Test5',
            'default_code': '',
            'product_family_id': False,
        })
        self.stage_id = self.env.ref('product_class.product_stage_data_1').id
        self.class_id = self.env.ref('product_class.product_class_data_1').id

    def test_onchange_stage(self):
        "Test onchange product stage"
        new_tmpl = self.prod_tmpl_obj.new({
            'product_stage_id': self.stage_id,
        })
        domain =\
            new_tmpl.onchange_stage().get('domain', {}).get('product_line_id')
        self.assertEqual(bool(domain), True)

    def test_onchange_line(self):
        "Test onchange product line"
        new_tmpl = self.prod_tmpl_obj.new({
            'product_line_id': self.product_tmpl.product_line_id.id,
        })
        domain =\
            new_tmpl.onchange_line().get('domain', {}).get('product_class_id')
        self.assertEqual(bool(domain), True)

    def test_onchange_class(self):
        "Test onchange product class"
        new_tmpl = self.prod_tmpl_obj.new({
            'product_class_id': self.product_tmpl.product_class_id.id,
        })
        domain = new_tmpl.onchange_class().get('domain',
                                               {}).get('product_family_id')
        self.assertEqual(bool(domain), True)

    def test_onchange_family(self):
        "Test onchange product family"
        new_tmpl = self.prod_tmpl_obj.new({
            'product_family_id': self.product_tmpl.product_family_id.id,
        })
        new_tmpl.onchange_family()
        self.assertEqual(new_tmpl.product_class_id.id, self.class_id)

    def test_generate_product_code(self):
        "Test product code based on sequence"
        self.product_tmpl.generate_product_code()
        self.assertEqual(bool(self.product_tmpl.default_code), True)

        with self.assertRaises(ValidationError):
            self.product_tmpl2.generate_product_code()
        with self.assertRaises(ValidationError):
            self.product_tmpl3.generate_product_code()
        with self.assertRaises(ValidationError):
            self.product_tmpl4.generate_product_code()
        with self.assertRaises(ValidationError):
            self.product_tmpl5.generate_product_code()


