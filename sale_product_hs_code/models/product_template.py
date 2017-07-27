# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)..

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_hs_code_id = fields.Many2one('product.hs.code', 'HS Name (CN)',
                                         ondelete='restrict', copy=False)
    hs_name = fields.Char(string='HS Name', related='product_hs_code_id.name',
                          readonly=True)
    hs_code = fields.Char(string='HS Code',
                          related='product_hs_code_id.hs_code',
                          readonly=True)
    hs_code_note = fields.Text(string='HS Code Note')
    hs_code_uom = fields.Many2one("product.uom", "HS UoM",
                                  related='product_hs_code_id.uom_id',
                                  help='Unit of Measure related to HS Code',
                                  readonly=True)

    @api.onchange('product_hs_code_id')
    def _onchange_product_hs_code_id(self):
        """Will catch the related hs code note if change hs code of product."""
        if self.product_hs_code_id:
            self.hs_code_note = self.product_hs_code_id.note
