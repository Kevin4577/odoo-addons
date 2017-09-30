# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError
import os


def _get_related_path(filename):
    if filename:
        return os.path.dirname(os.path.dirname(__file__)) + '/' + filename


@py3o_report.py3o_report_extender(
    report_xml_id='trading_stock_delivery_note_by_pallet.'
    'trading_stock_delivery_note_by_pallet_py3o')
def render_report_with_data(report_xml_id, data):
    """This function get the data from multi stock picking orders,
    and sum the product quantity and lot detail, in order to render the ods
    template with necessary data."""
    account_invoice = data['objects']
    lang = account_invoice.partner_id.lang
    base_invoice_export_obj = account_invoice.env['trading.invoice']
    py3o_multi_sheet_obj = account_invoice.env['report.py3o.multisheet']
    current_report = account_invoice.env.ref(
        'trading_stock_delivery_note_by_pallet.'
        'trading_stock_delivery_note_by_pallet_py3o')

    template_new = current_report.py3o_template_fallback_base
    tmp_folder_name = py3o_multi_sheet_obj._get_tmp_folder()
    py3o_multi_sheet_obj._create_tmp_folder(tmp_folder_name)
    template_new_path = tmp_folder_name + template_new
    current_report.write({
        'py3o_template_fallback': template_new_path
    })

    template_base = current_report.py3o_template_fallback_base
    template_base_path = _get_related_path(template_base)
    head_end_line = 9
    attribute_per_line = [
        '${line%d.client_order_ref}',
        '${line%d.product_id.customer_product_code}',
        '${line%d.product_id.name}',
        '${line%d.product_uom}',
        '${line%d.product_uom_qty}',
        '${line%d.qty_delivery}',
        '${line%d.carton_qty}',
    ]
    summary_line = [
        '${%s.sum_qty}',
        '${%s.sum_qty_delivery}',
        '${%s.pallet_sum}'
    ]
    stock_picking_obj = account_invoice.env['stock.picking']
    stock_picking_list = \
        stock_picking_obj.search([('invoice_id', '=', account_invoice.id)])
    if not stock_picking_list:
        raise ValidationError(_('Please specific delivery orders '
                                'for this account invoice.'))
    if account_invoice.invoice_line_ids.mapped('sale_line_ids'):
        lines_per_sheet = base_invoice_export_obj.\
            get_package_name_per_package_list(account_invoice)
        py3o_multi_sheet_obj.template_sheet_with_custom_line(
            head_end_line,
            lines_per_sheet,
            attribute_per_line,
            summary_line,
            template_new_path,
            template_base_path
        )
        package_list = base_invoice_export_obj.\
            get_pack_lot_list_per_package_type(account_invoice)
        index2 = 0
        for index1, package in enumerate(package_list['package_list']):
            pack_lot_lines_with_same_type = package[
                lines_per_sheet[index1]['name']]
            for pack_lot in pack_lot_lines_with_same_type:
                data[('line%d' % index2)] = pack_lot
                index2 += 1
        data.update({
            'partner_shipping_id':
                package_list['partner_shipping_id'].with_context(lang=lang),
            'package_no': package_list['package_no']
        })
    else:
        raise ValidationError(_('Please check whether this account invoice '
                                'was generated from sale order.'))
