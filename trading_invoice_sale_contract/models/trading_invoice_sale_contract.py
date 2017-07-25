# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(report_xml_id='trading_invoice_sale_contract'
                                  '.trading_invoice_sale_contract_py3o')
def render_template_with_data(report_xml_id, ctx):
    """This function get the data from sale order of specific stock picking,
     and sum the product quantity and price, in order to render the ods
     template with necessary data."""
    sale_order = ctx['objects']
    base_invoice_export_obj = sale_order.env['trading.invoice']
    ctx.update(base_invoice_export_obj.get_order_lines(sale_order))
