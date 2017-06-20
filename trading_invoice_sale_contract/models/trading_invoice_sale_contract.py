# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError
from odoo import _


@py3o_report.py3o_report_extender(report_xml_id='trading_invoice_sale_contract'
                                  '.trading_invoice_sale_contract_py3o')
def render_template_with_data(report_xml_id, ctx):
    """This function get the data from sale order of specific stock picking,
     and sum the product quantity and price, in order to render the ods
     template with necessary data."""
    stock_picking = ctx['objects']
    base_invoice_export_obj = stock_picking.env['trading.invoice']
    if stock_picking.sale_id:
        ctx.update(base_invoice_export_obj.get_order_lines(stock_picking))
    else:
        raise ValidationError(_('Please check whether this stock picking was'
                                ' generated from sale order.'))
