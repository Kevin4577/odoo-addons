# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class ProductClass(models.Model):
    "Data model of Product Class."
    _name = "product.class"
    _description = "Product Class"

    name = fields.Char('Name', index=True,
                       help='Class Name')
    code = fields.Char('Code', help='Class Code')
    line_id = fields.Many2one('product.line', 'Available Line',
                              help='Related Line')

    _sql_constraints = [('code_check', 'CHECK(length(code) < 2)',
                         _('The code length of the class must be 1.'))]
