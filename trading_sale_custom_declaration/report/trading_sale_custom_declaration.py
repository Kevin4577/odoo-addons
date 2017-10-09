# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.exceptions import ValidationError
import os
import math
from odoo.addons.report_py3o.models import py3o_report

HEAD_END_LINE = 20
LINES_PER_SHEET = 5
ATTRIBUTE_NUM_PER_LINE = 9
ATTRIBUTE_PER_LINE = ['${data.line%d.index}', '${data.line%d.hs_code.hs_code}',
                      '${data.line%d.hs_code.name}', '${data.line%d.qty}',
                      '${data.ship_to}', '',
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
    account_invoice = ctx['objects']
    data = {}
    current_report = account_invoice.env.ref(
        'trading_sale_custom_declaration.'
        'trading_sale_custom_declaration_py3o')
    py3o_multi_sheet_obj = account_invoice.env['report.py3o.multisheet']

    template_new = current_report.py3o_template_fallback_base
    tmp_folder_name = py3o_multi_sheet_obj._get_tmp_folder()
    py3o_multi_sheet_obj._create_tmp_folder(tmp_folder_name)
    template_new_path = tmp_folder_name + template_new
    current_report.write({
        'py3o_template_fallback': template_new_path
    })

    template_base = current_report.py3o_template_fallback_base
    template_base_path = _get_related_path(template_base)
    trading_sale_obj = account_invoice.env['trading.sale']
    sale_order_lines = account_invoice.invoice_line_ids.mapped('sale_line_ids')
    sale_order_list = sale_order_lines.mapped('order_id')
    stock_picking_obj = account_invoice.env['stock.picking']
    stock_picking_list = \
        stock_picking_obj.search([('invoice_id', '=', account_invoice.id)])
    if not stock_picking_list:
        raise ValidationError(_('Please specific delivery orders '
                                'for this account invoice.'))
    if sale_order_list:
        data['incoterms_id'] = account_invoice.incoterms_id
        data['pallet_sum'], gw_sum_witout_package, data['nw_sum'], \
            volume, package_list = \
            trading_sale_obj.get_product_stock_list(account_invoice)
        product_list = trading_sale_obj.\
            get_product_sale_list_with_pricelist(account_invoice)
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
                        'full_lines': LINES_PER_SHEET,
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
            trading_sale_obj.get_package_sum(account_invoice)
        data['gw_sum'] = gw_sum_witout_package + total_package_gw
        data['ship_to'] = \
            account_invoice.partner_shipping_id.country_id and \
            account_invoice.partner_shipping_id.country_id.name or ''
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this account '
                                'invoice was generated from'
                                ' sale order.'))
