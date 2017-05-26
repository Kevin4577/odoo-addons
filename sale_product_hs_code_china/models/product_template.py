# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)..

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_cn_name = fields.Char(string='HS Name (CN)',
                             related='product_hs_code_id.cn_name',
                             readonly=True)
    tax_code = fields.Many2one('account.tax', 'Rebate Rate',
                               related='product_hs_code_id.tax_id',
                               help='Tax Rebate Rate',
                               readonly=True)
