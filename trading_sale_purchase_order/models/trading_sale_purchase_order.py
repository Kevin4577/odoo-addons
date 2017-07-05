# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
import datetime
from openerp.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='trading_sale_purchase_order.'
                  'trading_sale_purchase_order_py3o')
def change_ctx(report_xml_id, ctx):
    """This function would gain the invoice, address and other data from
    sale order of specific stock picking, and sum the product quantity
    and price group by same hs code, in order to render the ods template
    with necessary data. """
    picking = ctx['objects']
    trading_sale_obj = picking.env['trading.sale']
    data = {}
    if picking.sale_id:
        data['so'] = picking.sale_id
        data['sum_qty'], data['sum_amount'], data['product_lines'] =\
            trading_sale_obj.get_product_sale_list(picking.sale_id)
        data['date'] = datetime.datetime.\
            strptime(picking.min_date, DEFAULT_SERVER_DATETIME_FORMAT
                     ) - relativedelta(days=30)
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this stock '
                                'picking was generated from sale '
                                'order.'))
