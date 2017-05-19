# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductHsCode(models.Model):

    _name = "product.hs.code"

    hs_code = fields.Char('HS Code', required=True)
    name = fields.Char('Name', required=True)
    uom_id = fields.Many2one('product.uom', 'Unit of Measure',
                             required=True)
    description = fields.Text('Additional Description')
    note = fields.Text('Declaration Note')
