# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, _
from odoo.exceptions import ValidationError
import os

HEAD_END_LINE = 20
LINES_PER_SHEET = 8
ATTRIBUTE_NUM_PER_LINE = 9
ATTRIBUTE_PER_LINE = ['${data.line%d.index}', '${data.line%d.hs_code.hs_code}',
                      '${data.line%d.hs_code.name}', '${data.line%d.qty}',
                      '${data.ship_to}', '${data.ship_from}',
                      '${data.line%d.unit_price}', '${data.line%d.total}',
                      '${data.line%d.pricelist}',
                      '${data.line%d.hs_code.cn_name}',
                      '${data.line%d.hs_code.uom_id.name}',
                      ]


class TradingSaleCustomDeclaration(models.Model):

    _inherit = 'ir.actions.report.xml'

    def _get_related_path(self, filename):
        """This function would generate the related path of template"""
        if filename:
            return os.path.dirname(os.path.dirname(__file__)) + '/' + filename

    @api.model
    def render_report(self, res_ids, name, data):
        """ This function would gain the invoice, address and other data from
        sale order of specific stock picking, and sum the product quantity
        and price group by same hs code, in order to render the ods template
        with necessary data."""
        action_py3o_report = self.search(
            [("report_name", "=", name),
             ("report_type", "=", "py3o")])
        existed_report = \
            self.env.ref('trading_sale_custom_declaration.'
                         'trading_sale_custom_declaration_py3o')
        if action_py3o_report and action_py3o_report.id == existed_report.id:
            template_new = \
                self.env.ref('trading_sale_custom_declaration.'
                             'trading_sale_custom_declaration_py3o'
                             ).py3o_template_fallback
            template_new_path = self._get_related_path(template_new)
            template_base = \
                self.env.ref('trading_sale_custom_declaration.'
                             'trading_sale_custom_declaration_py3o'
                             ).py3o_template_fallback_base
            template_base_path = self._get_related_path(template_base)
            trading_sale_obj = self.env['trading.sale']
            py3o_multi_sheet_obj = self.env['report.py3o.multisheet']
            stock_picking = self.env['stock.picking'].browse(res_ids)
            if stock_picking.sale_id:
                data['so'] = stock_picking.sale_id
                data['pallet_sum'], gw_sum_witout_package, data['nw_sum'], \
                    volume, package_list = \
                    trading_sale_obj.get_product_stock_list(stock_picking)
                product_list = trading_sale_obj.\
                    get_product_sale_list_with_pricelist(stock_picking.sale_id)
                total_line_num = len(product_list)
                for index, line in enumerate(product_list):
                    data[('line%d' % (index))] = line
                py3o_multi_sheet_obj.\
                    create_new_template(HEAD_END_LINE, LINES_PER_SHEET,
                                        total_line_num, ATTRIBUTE_NUM_PER_LINE,
                                        ATTRIBUTE_PER_LINE, template_new_path,
                                        template_base_path)
                package_qty, total_package_gw, package_meas = \
                    trading_sale_obj.get_package_sum(stock_picking)
                data['gw_sum'] = gw_sum_witout_package + total_package_gw
                data['ship_from'], data['ship_to'], data['ship_by'] =\
                    [stock_picking.ship_info_id.ship_from.country_id.name,
                     stock_picking.ship_info_id.ship_to.country_id.name,
                     stock_picking.ship_info_id.ship_by
                     ] if stock_picking.custom_check else[False, False, False]
            else:
                raise ValidationError(_('Please check whether this stock '
                                        'picking was generated from'
                                        ' sale order.'))
        return super(TradingSaleCustomDeclaration, self
                     ).render_report(res_ids, name, data)
