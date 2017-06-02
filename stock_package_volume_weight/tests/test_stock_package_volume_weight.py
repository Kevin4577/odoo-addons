# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestStockPackageVolumeWeight(common.TransactionCase):

    def setUp(self):
        super(TestStockPackageVolumeWeight, self).setUp()
        self.product_packaging_obj = self.env['product.packaging']
        self.stock_quant_package_obj = self.env['stock.quant.package']

#        Create Product Packaging
        self.product_packaging = self.product_packaging_obj.\
            create({'name': 'Test Product Packaging',
                    'qty': 5,
                    'weight': 10.0,
                    'carton_qty': 7.0,
                    })

#        Create Stock Quant Package
        self.stock_quant_package = self.stock_quant_package_obj.\
            create({'packaging_id': self.product_packaging.id,
                    })

    def test_onchange_packaging_id(self):
        """To set weight,carton_qty fields based on product packaging"""
        self.assertNotEqual(self.product_packaging.weight,
                            self.stock_quant_package.weight)
        self.assertNotEqual(self.product_packaging.carton_qty,
                            self.stock_quant_package.carton_qty)
        self.stock_quant_package._onchange_packaging_id()
        self.assertEqual(self.product_packaging.weight,
                         self.stock_quant_package.weight)
        self.assertEqual(self.product_packaging.carton_qty,
                         self.stock_quant_package.carton_qty)
