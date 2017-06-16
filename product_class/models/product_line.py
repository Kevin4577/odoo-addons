# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class ProductLine(models.Model):
    "Data model of Product Line."
    _name = "product.line"
    _description = "Product Line"

    name = fields.Char('Name', index=True,
                       help='Line Name')
    code = fields.Char('Code', help='Line Code')
    stage_ids = fields.Many2many('product.stage', 'product_stage_rel',
                                 'line_id', 'stage_id', 'Available Stage',
                                 help='Related Stage')
    class_ids = fields.Many2many('product.class', 'product_class_line_rel',
                                 'p_line_id',
                                 'class_id', 'Available Class',
                                 help='Related Class')

    _sql_constraints = [('code_check', 'CHECK(length(code) < 2)',
                         _('The code length of the line must be 1.'))]

    _sql_constraints = [('code_uniq', 'UNIQUE(code)',
                         _('The code of the line must be unique.'))]
