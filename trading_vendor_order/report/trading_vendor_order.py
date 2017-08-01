# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.exceptions import ValidationError
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='trading_vendor_order.trading_vendor_order_py3o')
def render_report_with_data(report_xml_id, data):
    """This function get order lines from purchase orders, and sum the quantity
    and price amount, in order to render the ods template with
    necessary data.."""
    purchase_order_list = data['objects']
    partner_list = list(purchase_order_list.mapped('partner_id').ids)
    if len(partner_list) > 1:
        raise ValidationError(_('Please check whether all purchase orders '
                                'belong to one vendor.'))
    trading_vendor_obj = purchase_order_list.env['trading.vendor']
    vendor_contact_person = trading_vendor_obj.\
        get_purchase_order_vendor_contact(purchase_order_list[0])
    company_contact_person = trading_vendor_obj.\
        get_purchase_order_company_contact(purchase_order_list[0])
    qty_total, price_total = trading_vendor_obj.\
        get_purchase_order_list_total_quantity_and_price(purchase_order_list)
    data.update(vendor_contact_person)
    data.update(company_contact_person)
    data.update({'qty_total': qty_total,
                 'price_total': price_total,
                 'object': purchase_order_list[0]})
