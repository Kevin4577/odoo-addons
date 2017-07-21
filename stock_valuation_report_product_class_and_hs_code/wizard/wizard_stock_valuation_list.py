# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _


class WizardStockValuationList(models.TransientModel):
    _inherit = 'wizard.stock.valuation.list'

    def _get_product_inventory_from_product_class(self, stock_history):
        """
            Filter the stock history with selected product class from context
        :param stock_history:
        :return:
        """

        if self._context.get('product_stage_id', False) \
                and self._context.get('product_line_id', False) \
                and self._context.get('product_class_id', False) \
                and self._context.get('product_family_id', False):
            stock_history_new = stock_history.filtered(
                lambda r:
                r.product_id.product_stage_id.id == self._context.get(
                    'product_stage_id')
                and r.product_id.product_line_id.id == self._context.get(
                    'product_line_id')
                and r.product_id.product_class_id.id == self._context.get(
                    'product_class_id')
                and r.product_id.product_family_id.id == self._context.get(
                    'product_family_id')
            )
            return stock_history_new
        else:
            return stock_history

    def _get_product_inventory_from_hs_code(self, stock_history):
        """
            Filter the stock history with selected hs code from context
        :param stock_history:
        :return:
        """

        if self._context.get('hs_code', False):
            stock_history_new = stock_history.filtered(
                lambda r:
                r.product_id.product_hs_code_id.id == self._context.get(
                    'hs_code')
            )
            return stock_history_new
        else:
            return stock_history

    def _get_product_inventory_additonal_filter(self, stock_history):
        """
            This function could be inherited to filter stock history
            list by additional options.
        """
        if self._context.get('product_stage_id', False) \
                and self._context.get('product_line_id', False) \
                and self._context.get('product_class_id', False) \
                and self._context.get('product_family_id', False):
            stock_history = \
                self._get_product_inventory_from_product_class(stock_history)

        if self._context.get('hs_code', False):
            stock_history = \
                self._get_product_inventory_from_hs_code(stock_history)

        return super(WizardStockValuationList, self).\
            _get_product_inventory_additonal_filter(stock_history)

    def _get_stock_valuation_line_additional_value(self, product):
        """
            This function could be extended to add more values to generate
            stock valuation report
        :param product:
        :return:
        """

        res = super(WizardStockValuationList, self).\
            _get_stock_valuation_line_additional_value(product)
        res.update(
            {

                'product_hs_code_name':
                    product['product'].product_hs_code_id.hs_code,
                'product_stage_name':
                    product['product'].product_stage_id.name,
                'product_line_name':
                    product['product'].product_line_id.name,
                'product_class_name':
                    product['product'].product_class_id.name,
                'product_family_name':
                    product['product'].product_family_id.name,

            }
        )
        return res

    def _get_table_title(self):
        """
            Save the format in col:title to show on the stock valuation report
            view
        :return:
        """

        title = super(WizardStockValuationList, self)._get_table_title()

        title.update({
            0: _("HS Code"),
            1: _("Default Code"),
            2: _("Product Name"),
            3: _("Product Stage"),
            4: _("Product Line"),
            5: _("Product Class"),
            6: _("Product Family"),
            7: _("Unit of Measure"),
            8: _("Inventory Balance Before Start Date"),
            9: _("Incoming Inventory Balance"),
            10: _("Outgoing Inventory Balance"),
            11: _("Inventory Balance Before End Date"),
            12: _("Safety Stock Level"),
            13: _("Below Safety Stock"),
            14: _("Location Name")
        })
        return title

    @api.multi
    def xlsx_export(self):
        """
            Produce xlsx report based on the data report produced
        :return:
        """

        data = super(WizardStockValuationList, self).xlsx_export()
        data.update({
            'report_name': 'stock.valuation.report.xlsx.product.class.hs.code'
        })
        return data


class WizardStockValuationLine(models.TransientModel):
    _inherit = 'wizard.stock.valuation.line'

    product_hs_code_name = fields.Char(
        'HS Code Name',
        readonly=True,
        default="",
        help='HS Code Name'
    )
    product_stage_name = fields.Char(
        'Product Stage Name',
        readonly=True,
        default="",
        help='Product Stage Name'
    )
    product_line_name = fields.Char(
        'Product Line Name',
        readonly=True,
        default="",
        help='Product Line Name'
    )
    product_class_name = fields.Char(
        'Product Class Name',
        readonly=True,
        default="",
        help='Product Class Name'
    )
    product_family_name = fields.Char(
        'Product Family Name',
        readonly=True,
        default="",
        help='Product Family Name'
    )
