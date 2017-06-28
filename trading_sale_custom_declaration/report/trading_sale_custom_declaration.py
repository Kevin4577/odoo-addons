# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.exceptions import ValidationError
import os
import math
from odoo.addons.report_py3o.models import py3o_report

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


def _update_base_template(
        sheet_lines_data,
        py3o_multi_sheet_obj,
        template_base_path,
        template_new_path
):
    doc = py3o_multi_sheet_obj.open_base_template(
        template_base_path)
    sheets = doc.sheets
    py3o_multi_sheet_obj.multi_sheet_per_template(
        sheets, sheet_lines_data)
    py3o_multi_sheet_obj.multi_lines_per_sheet(
        sheets, sheet_lines_data)
    py3o_multi_sheet_obj.multi_attribute_per_line(
        sheets,
        sheet_lines_data,
        ATTRIBUTE_PER_LINE,
        ATTRIBUTE_NUM_PER_LINE)
    py3o_multi_sheet_obj.save_new_template(
        template_new_path,
        doc
    )


def _get_related_path(filename):
    """This function would generate the related path of template"""
    if filename:
        return os.path.dirname(os.path.dirname(__file__)) + '/' + filename


@py3o_report.py3o_report_extender(
    report_xml_id='trading_sale_custom_declaration.'
                  'trading_sale_custom_declaration_py3o')
def change_ctx(report_xml_id, ctx):
    """ This function would gain the invoice, address and other data from
        sale order of specific stock picking, and sum the product quantity
        and price group by same hs code, in order to render the ods template
        with necessary data."""
    picking = ctx['objects']
    data = {}
    template_new = \
        picking.env.ref('trading_sale_custom_declaration.'
                        'trading_sale_custom_declaration_py3o'
                        ).py3o_template_fallback
    template_new_path = _get_related_path(template_new)
    template_base = \
        picking.env.ref('trading_sale_custom_declaration.'
                        'trading_sale_custom_declaration_py3o'
                        ).py3o_template_fallback_base
    template_base_path = _get_related_path(template_base)
    trading_sale_obj = picking.env['trading.sale']
    py3o_multi_sheet_obj = picking.env['report.py3o.multisheet']
    if picking.sale_id:
        data['so'] = picking.sale_id
        data['pallet_sum'], gw_sum_witout_package, data['nw_sum'], \
            volume, package_list = \
            trading_sale_obj.get_product_stock_list(picking)
        product_list = trading_sale_obj.\
            get_product_sale_list_with_pricelist(picking.sale_id)
        sheet_lines_data = {}
        lines_per_lines = int(math.ceil(
            len(ATTRIBUTE_PER_LINE) / float(ATTRIBUTE_NUM_PER_LINE
                                            )))
        for index, line in enumerate(product_list):
            data[('line%d' % (index))] = line
            sheet_name = 'sheet%d' % (index / LINES_PER_SHEET)
            if not sheet_lines_data.get(sheet_name, False):
                sheet_lines_data[sheet_name] = {}
                sheet_lines_data[sheet_name].\
                    update({
                        'name': sheet_name,
                        'sequence': (index / LINES_PER_SHEET),
                        'duplicate': True,
                        'lines': lines_per_lines,
                        'head_end_line': HEAD_END_LINE,
                    })
            else:
                sheet_lines_data[sheet_name]['lines'] += lines_per_lines

        _update_base_template(
            sheet_lines_data,
            py3o_multi_sheet_obj,
            template_base_path,
            template_new_path
        )
        package_qty, total_package_gw, package_meas = \
            trading_sale_obj.get_package_sum(picking)
        data['gw_sum'] = gw_sum_witout_package + total_package_gw
        data['ship_from'], data['ship_to'], data['ship_by'] =\
            [picking.ship_info_id.ship_from.country_id.name,
             picking.ship_info_id.ship_to.country_id.name,
             picking.ship_info_id.ship_by
             ] if picking.custom_check else[False, False, False]
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this stock '
                                'picking was generated from'
                                ' sale order.'))
