# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api
from odoo.addons.report_py3o.models import py3o_report


@api.multi
def get_stock_picking_total_product_quantity(stock_picking):
    """This function return the total quantity of returned products of
    specific stock picking."""
    qty_total = 0
    for pack_id in stock_picking.pack_operation_product_ids:
        qty_total += pack_id.qty_done
    return qty_total


@py3o_report.py3o_report_extender(report_xml_id='trading_vendor_return_order.'
                                  'trading_vendor_return_order_py3o')
def render_report_with_data(report_xml_id, data):
    """This function generates the return stock picking orders of related
    purchase orders. And display the returned product list, and sum of
    quantity of those products."""
    stock_picking_list = data['objects']
    return_stock_picking_list = []
    for stock_picking in stock_picking_list:
        qty_total = get_stock_picking_total_product_quantity(stock_picking)
        return_stock_picking_list.append({'qty_total': qty_total,
                                          'order': stock_picking
                                          })
    data.update({'return_stock_picking_list': return_stock_picking_list})
