# -*- coding: utf-8 -*-
# © 2016 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo.tests import common


class TestShipping(common.TransactionCase):

    def setUp(self):
        super(TestShipping, self).setUp()
        self.ship_from = self.env.ref("base.res_partner_1")
        self.ship_to = self.env.ref("base.res_partner_1")
        self.shipping = self.env['shipping'].create({
            'name': 'Test Shipping',
            'ship_from': self.ship_from.id,
            'ship_to': self.ship_to.id,
            'ship_by': 'Ship By'
        })

    def test_name_get(self):
        "This method check display name"
        res = self.shipping.name_get()
        for r in res:
            self.assertTrue(r[1], 'Should have display name')
        return res
