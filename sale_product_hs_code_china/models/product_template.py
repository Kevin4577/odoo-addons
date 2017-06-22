# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)..

from odoo import api, fields, models
from lxml import etree


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_cn_name = fields.Char(string='HS Name (CN)',
                             related='product_hs_code_id.cn_name',
                             readonly=True)
    tax_code = fields.Many2one('account.tax', 'Rebate Rate',
                               related='product_hs_code_id.tax_id',
                               help='Tax Rebate Rate',
                               readonly=True)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        """Fields view get method for invisible hs_name or hs_cn_name
        based on groups."""
        res = super(ProductTemplate,
                    self).fields_view_get(view_id=view_id,
                                          view_type=view_type,
                                          toolbar=toolbar,
                                          submenu=submenu)
        if view_type != 'form':
            return res
        user_obj = self.env['res.users']
        hs_code_mang_grp_id = user_obj.has_group('sale_product_hs_code'
                                                 '.group_hs_code_manager')
        if hs_code_mang_grp_id:
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='hs_cn_name']"):
                node.set("modifiers", '{"invisible": true}')
            res['arch'] = etree.tostring(doc)
        return res
