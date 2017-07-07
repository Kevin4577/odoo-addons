# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError
from odoo import _


@py3o_report.py3o_report_extender(report_xml_id='trading_stock_delivery_note.'
                                  'trading_stock_delivery_note_py3o')
def render_template_with_data(report_xml_id, ctx):
    """This function get order lines from sale orders of stock picking list,
    and sum the order quantity and delivery quantity, in order to render the
    ods template with necessary data.."""
    stock_picking_list = ctx['objects']
    if len(stock_picking_list.mapped('partner_id').ids) > 1:
        raise ValidationError(_('Please check whether all delivery orders'
                                ' belong to one customer.'))
    if stock_picking_list.filtered(lambda stock_picking:
                                   stock_picking.state != 'done'):
        raise ValidationError(_('Please check the state of stock picking.'))
    base_invoice_export_obj = stock_picking_list.env['trading.invoice']
    if not stock_picking_list.filtered(lambda stock_picking:
                                       not stock_picking.sale_id):
        ctx.update(base_invoice_export_obj.get_product_order_list_with_qty
                   (stock_picking_list))
    else:
        raise ValidationError(_('Please check whether this stock picking was'
                                ' generated from sale order.'))
