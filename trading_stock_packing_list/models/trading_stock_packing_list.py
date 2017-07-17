# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.report_py3o.models import py3o_report
from odoo.exceptions import ValidationError
from odoo import _


@py3o_report.py3o_report_extender(report_xml_id='trading_stock_packing_list'
                                  '.trading_stock_packing_list_py3o')
def render_template_with_data(report_xml_id, data):
    """This function get the data from delivery order lines related to
    selected account invoice, and sum the carton quantity, grow weight,
    and net weight, in order to render the ods template with necessary data."""
    account_invoice = data['objects']
    base_invoice_export_obj = account_invoice.env['trading.invoice']
    if account_invoice and account_invoice.invoice_line_ids:
        data.update(
            base_invoice_export_obj.get_detail_lot_list_per_invoice(
                account_invoice)
        )
    else:
        raise ValidationError(_('Please check whether this stock picking was'
                                ' generated from sale order.'))
