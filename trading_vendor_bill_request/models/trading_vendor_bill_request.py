# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api
from odoo.addons.report_py3o.models import py3o_report


@api.multi
def get_partner_bank(res_partner):
    """This function return the bank information of partner."""
    bank_name = ''
    bank_account = ''
    if res_partner.bank_ids:
        bank_name = res_partner.bank_ids[0].bank_name
        bank_account = res_partner.bank_ids[0].acc_number
    return bank_name, bank_account


@py3o_report.py3o_report_extender(report_xml_id='trading_vendor_bill_request.'
                                  'trading_vendor_bill_request_py3o')
def render_report_with_data(report_xml_id, data):
    """This function get the company contact person and bank account, in order
    to render the ods template with necessary data."""
    account_invoice = data['objects']
    trading_vendor_obj = account_invoice.env['trading.vendor']
    contact_name, contact_email =\
        trading_vendor_obj.get_partner_contact(account_invoice.partner_id)
    bank_name, bank_account = get_partner_bank(account_invoice.partner_id)
    data.update({
        'company_contact_name': contact_name,
        'company_bank_name': bank_name,
        'company_bank_account': bank_account,
    })
