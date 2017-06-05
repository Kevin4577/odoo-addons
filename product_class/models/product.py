# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, _


class ProductProduct(models.Model):
    "Data model of Product Template."
    _inherit = "product.product"

    _sql_constraints = [('default_code_uniq', 'UNIQUE(default_code)',
                         _('The default code of the product must be unique.'))]
