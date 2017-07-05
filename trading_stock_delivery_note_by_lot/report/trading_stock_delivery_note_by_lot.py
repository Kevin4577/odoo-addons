# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError


@py3o_report.py3o_report_extender(
    report_xml_id='trading_stock_delivery_note_by_lot.'
    'trading_stock_delivery_note_by_lot_py3o')
def render_report_with_data(report_xml_id, ctx):
    """This function get the data from sale order of specific stock
    picking, and sum the carton quantity and weight, in order to render the
    ods template with necessary data."""
    stock_picking_list = ctx['objects']
    if len(stock_picking_list.mapped('partner_id').ids) > 1:
        raise ValidationError(_('Please check whether all delivery '
                                'orders period belong to one customer'))
    base_invoice_export_obj = stock_picking_list.env['trading.invoice']
    if stock_picking_list.filtered(lambda stock_picking:
                                   stock_picking.sale_id):
        ctx.update(base_invoice_export_obj.
                   get_product_lot_list_per_sale_order(stock_picking_list))
    else:
        raise ValidationError(_('Please check whether this stock picking '
                                'was generated from sale order.'))
