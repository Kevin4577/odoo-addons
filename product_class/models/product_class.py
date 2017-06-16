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
    line_ids = fields.Many2many(comodel_name='product.line',
                                string='Available Line',
                                help='Related Line')
    family_ids = fields.Many2many(comodel_name='product.family',
                                  string='Available Family',
                                  help='Related Family')

    _sql_constraints = [('code_check', 'CHECK(length(code) < 2)',
                         _('The code length of the class must be 1.'))]

    _sql_constraints = [('code_uniq', 'UNIQUE(code)',
                         _('The code of the class must be unique.'))]
