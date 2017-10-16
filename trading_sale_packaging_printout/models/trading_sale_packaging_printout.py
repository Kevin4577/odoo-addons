# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.tools import float_repr
from odoo.exceptions import ValidationError
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='trading_sale_packaging_printout.'
    'trading_sale_packaging_printout_py3o')
def change_ctx(report_xml_id, ctx):
    """This function would get the package information,
        lot and other data from stock operation of the specific stock
        picking(s), and sum the package quantity,
        grow weight and meas of those package,
        in order to render the ods template """
    data = {}
    account_invoice = ctx['objects']
    case_weight_precision = \
        account_invoice.env['decimal.precision'].precision_get(
            'Case Weight Printout'
        )
    case_volume_precision = \
        account_invoice.env['decimal.precision'].precision_get(
            'Case Volume Printout'
        )
    trading_sale_obj = account_invoice.env['trading.sale']
    sale_order_lines = account_invoice.invoice_line_ids.mapped('sale_line_ids')
    sale_order_list = sale_order_lines.mapped('order_id')
    stock_picking_obj = account_invoice.env['stock.picking']
    stock_picking_list = \
        stock_picking_obj.search([('invoice_id', '=', account_invoice.id)])
    lang = account_invoice.partner_id.lang
    if not stock_picking_list:
        raise ValidationError(_('Please specific delivery orders '
                                'for this account invoice.'))
    if sale_order_list:
        data['pallet_sum'], gw_sum_witout_package, data['nw_sum'],\
            meas_sum_witout_package, data['product_lines'] =\
            trading_sale_obj.get_product_stock_list(account_invoice)
        data['qty_package'], data['total_package_gw'],\
            data['total_package_meas'] =\
            trading_sale_obj.get_package_sum(account_invoice)
        data['gw_sum'] = \
            float_repr(
                gw_sum_witout_package + float(data['total_package_gw']),
                precision_digits=case_weight_precision
            )
        data['meas_sum'] = \
            float_repr(
                meas_sum_witout_package + float(data['total_package_meas']),
                precision_digits=case_volume_precision
            )
        data['company_country_name'] = \
            account_invoice.company_id.with_context(lang=lang).country_id.name
        data['shipping_country_name'] = \
            account_invoice.partner_shipping_id.with_context(
                lang=lang
        ).country_id.name if account_invoice.partner_shipping_id else '--'
        ctx['data'].update(trading_sale_obj.get_date_invoice(account_invoice))
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this account '
                                'invoice was generated from sale '
                                'order.'))
