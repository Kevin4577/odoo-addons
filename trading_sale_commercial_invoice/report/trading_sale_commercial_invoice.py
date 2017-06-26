# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.exceptions import ValidationError
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='trading_sale_commercial_invoice.'
                  'trading_sale_commercial_invoice_py3o'
)
def change_ctx(report_xml_id, ctx):
    stock_picking = ctx['objects']
    trading_sale_obj = stock_picking.env['trading.sale']
    data = {}
    if stock_picking.sale_id:
        data['so'] = stock_picking.sale_id
        data['sum_qty'], data['sum_amount'], data['product_lines'] = \
            trading_sale_obj. \
            get_product_sale_list(stock_picking.sale_id)
        data['pallet_sum'], gross_weight, net_weight, volume, \
            package_list = \
            trading_sale_obj. \
            get_product_stock_list(stock_picking)
        data['ship_from'], data['ship_to'], data['ship_by'] = \
            [stock_picking.ship_info_id.ship_from.country_id.name,
             stock_picking.ship_info_id.ship_to.country_id.name,
             stock_picking.ship_info_id.ship_by
             ] if stock_picking.custom_check else [False, False, False]
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this stock '
                                'picking was generated from sale'
                                ' order.'))
