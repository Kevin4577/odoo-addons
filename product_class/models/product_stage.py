# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class ProductStage(models.Model):
    "Data model of Product Stage."
    _name = "product.stage"
    _description = "Product Stage"

    name = fields.Char('Name', index=True,
                       help='Stage Name')
    code = fields.Char('Code', help='Stage Code')

    _sql_constraints = [('code_check', 'CHECK(length(code) < 2)',
                         _('The code length of the stage must be 1.'))]
