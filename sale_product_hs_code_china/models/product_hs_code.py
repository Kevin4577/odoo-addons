# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductHsCode(models.Model):
    _inherit = "product.hs.code"

    cn_name = fields.Char('Name (CN)', required=True, help='Chinese Name')
    tax_id = fields.Many2one('account.tax', 'Rebate Rate',
                             required=True, help='Tax Rebate Rate')
