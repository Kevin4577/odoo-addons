# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from openerp.exceptions import ValidationError


class ProductHsCode(models.Model):
    _inherit = "product.hs.code"

    cn_name = fields.Char('Name (CN)', help='Chinese Name')
    tax_id = fields.Many2one('account.tax', 'Rebate Rate',
                             help='Tax Rebate Rate')
    english_uom_id = fields.Many2one('product.uom', 'English HS UoM',
                                     help='English Unit of Measure.')

    @api.multi
    def name_get(self):
        return [(hs_code.id, "%s-%s" % (hs_code.hs_code,
                                        hs_code.cn_name,
                                        )) for hs_code in self]

    @api.constrains('hs_code', 'cn_name')
    def _check_hs_code_cn_name(self):
        if self.hs_code and self.cn_name:
            hs_code_rec = self.search([('hs_code', '=', self.hs_code),
                                       ('cn_name', '=', self.cn_name),
                                       ('id', '!=', self.id)])
            if hs_code_rec:
                raise ValidationError(_("The HS Code must be unique."))
