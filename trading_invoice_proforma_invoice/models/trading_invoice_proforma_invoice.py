# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError
from odoo import _


@py3o_report.py3o_report_extender(report_xml_id='trading_'
                                  'invoice_proforma_invoice.trading_'
                                  'invoice_proforma_invoice_py3o')
def render_template_with_data(report_xml_id, ctx):
    """This function get the data from sale order of account invoice,
    and sum the invoice quantity, unit price, and amount, in order to render
    the ods template with necessary data."""
    sale_order = ctx['objects']
    base_invoice_export_obj = sale_order.env['trading.invoice']
    if sale_order.order_line:
        ctx.update(base_invoice_export_obj.get_invoice_lines_per_invoice
                   (sale_order))
        ctx.update(
            {
                'confirmation_date':
                    sale_order.confirmation_date and
                    base_invoice_export_obj.
                get_date(sale_order.confirmation_date) or False,
                'requested_date':
                    sale_order.requested_date and
                    base_invoice_export_obj.get_date(
                        sale_order.requested_date
                ) or False
            }
        )
        ctx.update(base_invoice_export_obj.get_customer(ctx['company']))
    else:
        raise ValidationError(_('Please check whether this account invoice '
                                'was generated from sale order.'))
