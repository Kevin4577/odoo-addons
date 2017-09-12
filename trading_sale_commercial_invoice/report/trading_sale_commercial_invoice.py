# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.exceptions import ValidationError
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='trading_sale_commercial_invoice.'
                  'trading_sale_commercial_invoice_py3o'
)
def change_ctx(report_xml_id, ctx):
    account_invoice = ctx['objects']
    trading_sale_obj = account_invoice.env['trading.sale']
    sale_order_lines = account_invoice.invoice_line_ids.mapped('sale_line_ids')
    sale_order_list = sale_order_lines.mapped('order_id')
    stock_picking_obj = account_invoice.env['stock.picking']
    stock_picking_list = \
        stock_picking_obj.search([('invoice_id', '=', account_invoice.id)])
    data = {}
    if not stock_picking_list:
        raise ValidationError(_('Please specify delivery orders '
                                'for this account invoice.'))
    if sale_order_list:
        data['sum_qty'], data['sum_amount'], data['product_lines'] = \
            trading_sale_obj. \
            get_product_sale_list(account_invoice)
        data['pallet_sum'], gross_weight, net_weight, volume, \
            package_list = \
            trading_sale_obj. \
            get_product_stock_list(account_invoice)
        ctx['data'].update(trading_sale_obj.get_date_invoice(account_invoice))
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this account '
                                'invoice was generated from sale'
                                ' order.'))
