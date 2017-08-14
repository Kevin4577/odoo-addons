# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductHsCode(models.Model):
    _name = "product.hs.code"
    _description = "Product HS Code"
    _rec_name = 'name'

    hs_code = fields.Char('HS Code', copy=False)
    name = fields.Char('Name')
    uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    description = fields.Text('Additional Description')
    note = fields.Text('Declaration Note')
