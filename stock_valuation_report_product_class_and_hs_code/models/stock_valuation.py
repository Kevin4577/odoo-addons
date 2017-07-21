# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class StockValuation(models.Model):
    _inherit = 'stock.valuation'

    @api.model
    def _selection_filter_by_product_class(self):
        """
            Get the list of filter allowed according to the options checked
        in 'Settings-Warehouse'.
        :return:
        """
        res_filter = [
            ('none', _('All Product Class'))
        ]
        if self.user_has_groups('sale_product_hs_code.group_hs_code_user'):
            res_filter.append(
                ('product_class', _('Manual selection of product class')))
        return res_filter

    @api.model
    def _selection_filter_by_hs_code(self):
        """
            Get the list of filter allowed according to the options checked
        in 'Settings-Warehouse'.
        :return:
        """
        res_filter = [
            ('none', _('All HS Code'))
        ]
        if self.user_has_groups('sale_product_hs_code.group_hs_code_user'):
            res_filter.append(('hs_code', _('One HS code only')))
        return res_filter

    filter_by_product_class = fields.Selection(
        selection='_selection_filter_by_product_class',
        string='Filter By Product Class',
        required=True,
        default='none',
        help="If you do the valuation, you can choose 'All Product Class' for "
             "Any combination of product class of product, 'Manual Selection "
             "of Product Class' for specific combination of product class."
    )

    filter_by_hs_code = fields.Selection(
        selection='_selection_filter_by_hs_code',
        string='Filter By HS Code',
        required=True,
        default='none',
        help="If you do the valuation, you can choose 'All HS Code' for any HS"
             "code of product 'one HS Code' for hs code of product."
    )

    product_stage_id = fields.Many2one('product.stage',
                                       'Product Stage', ondelete='restrict',
                                       help='Product Stage', index=True)
    product_line_id = fields.Many2one('product.line', 'Product Line',
                                      ondelete='restrict',
                                      help='Product Line', index=True)
    product_class_id = fields.Many2one('product.class',
                                       'Product Class', ondelete='restrict',
                                       help='Product Class', index=True)
    product_family_id = fields.Many2one('product.family',
                                        'Product Family', ondelete='restrict',
                                        help='Product Family', index=True)
    product_hs_code_id = fields.Many2one('product.hs.code', 'HS Code',
                                         ondelete='restrict', copy=False)

    @api.onchange('filter_by_product_class')
    def onchange_filter_by_product_class(self):
        if self.filter_by_product_class != 'product_class':
            self.product_stage_id = False
            self.product_line_id = False
            self.product_class_id = False
            self.product_family_id = False

    @api.onchange('filter_by_hs_code')
    def onchange_filter_by_hs_code(self):
        if self.filter_by_hs_code != 'hs_code':
            self.product_hs_code_id = False

    @api.multi
    def prepare_valuation(self):
        """
            Redirect to wizard of stock valuation report with some selected
            fields from user
        :return:
        """

        res = super(StockValuation, self).prepare_valuation()
        if res.get('context', False):
            res['context'].update(
                {
                    'product_stage_id': self.product_stage_id and
                    self.product_stage_id.id or False,
                    'product_line_id': self.product_line_id and
                    self.product_line_id.id or False,
                    'product_class_id': self.product_class_id and
                    self.product_class_id.id or False,
                    'product_family_id': self.product_family_id and
                    self.product_family_id.id or False,
                    'hs_code': self.product_hs_code_id and
                    self.product_hs_code_id.id or False,
                }
            )
        return res
