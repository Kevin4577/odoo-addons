# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductHsCode(models.Model):
    _inherit = "product.hs.code"
    _rec_name = 'cn_name'

    cn_name = fields.Char('Name (CN)', help='Chinese Name')
    tax_id = fields.Many2one('account.tax', 'Rebate Rate',
                             help='Tax Rebate Rate')
