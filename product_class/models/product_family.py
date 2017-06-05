# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class ProductFamily(models.Model):
    "Data model of Product Family."
    _name = "product.family"
    _description = "Product Family"

    name = fields.Char('Name', index=True,
                       help='Family Name')
    code = fields.Char('Code', help='Family Code')
    class_id = fields.Many2one('product.class', 'Available Class',
                               help='Related Class')

    _sql_constraints = [('code_check',
                         'CHECK(length(code) < 3 and length(code) >1)',
                         _('The code length of the family must be 2.'))]
