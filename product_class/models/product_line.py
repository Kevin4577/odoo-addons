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
    code = fields.Char('Code', copy=False, help='Line Code')
    stage_ids = fields.Many2many(comodel_name='product.stage',
                                 string='Available Stage',
                                 help='Related Stage',
                                 ondelete='restrict')
    class_ids = fields.Many2many(comodel_name='product.class',
                                 string='Available Class',
                                 help='Related Class',
                                 ondelete='restrict')

    _sql_constraints = [('code_check', 'CHECK(length(code) < 2)',
                         _('The code length of the line must be 1.')),
                        ('code_uniq', 'UNIQUE(code)',
                         _('The code of the line must be unique.'))
                        ]
