# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError
from odoo import _


@py3o_report.py3o_report_extender(report_xml_id='trading_commercial_invoice.'
                                  'trading_commercial_invoice_py3o')
def render_template_with_data(report_xml_id, ctx):
    """This function get the data from sale order of account invoice,
    quantity and unit price, in order to render the ods template
    with necessary data."""
    account_invoice = ctx['objects']
    base_invoice_export_obj = account_invoice.env['trading.invoice']
    if account_invoice.invoice_line_ids:
        lang = account_invoice.partner_id.lang
        ctx.update(base_invoice_export_obj.get_order_lines_per_invoice
                   (account_invoice))
        ctx.update(base_invoice_export_obj.get_customer(
            account_invoice.company_id, lang))
        ctx.update(
            {
                'country_name':
                    account_invoice.with_context(
                        lang=lang
                    ).partner_id.country_id.name,
                'payment_term_id':
                    account_invoice.payment_term_id.with_context(
                        lang=lang
                    ),
                'shipping_country_name':
                    account_invoice.with_context(
                        lang=lang
                    ).partner_shipping_id.country_id.name,
                'number':
                    account_invoice.number if account_invoice.number else '--'
            }
        )
        ctx.update(base_invoice_export_obj.get_date_invoice(account_invoice))
    else:
        raise ValidationError(_('Please check whether this account invoice'
                                ' was generated from sale order.'))
