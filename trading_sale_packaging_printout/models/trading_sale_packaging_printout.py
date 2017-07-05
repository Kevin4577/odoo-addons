# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.exceptions import ValidationError
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='trading_sale_packaging_printout.'
    'trading_sale_packaging_printout_py3o')
def change_ctx(report_xml_id, ctx):
    """This function would get the package information,
        lot and other data from stock operation of the specific stock
        picking(s), and sum the package quantity,
        grow weight and meas of those package,
        in order to render the ods template """
    data = {}
    picking = ctx['objects']
    trading_sale_obj = picking.env['trading.sale']
    available_picking_state = ['assigned', 'partially_available',
                               'done']
    if picking.state not in available_picking_state:
        raise ValidationError(_('Please first confirm your stock '
                                'picking state.'))
    if picking.sale_id:
        data['so'] = picking.sale_id
        data['pallet_sum'], gw_sum_witout_package, data['nw_sum'],\
            meas_sum_witout_package, data['product_lines'] =\
            trading_sale_obj.get_product_stock_list(picking)
        data['qty_package'], data['total_package_gw'],\
            data['total_package_meas'] =\
            trading_sale_obj.get_package_sum(picking)
        data['gw_sum'] =\
            gw_sum_witout_package + data['total_package_gw']
        data['meas_sum'] =\
            meas_sum_witout_package + data['total_package_meas']
        data['ship_from'], data['ship_to'], data['ship_by'] =\
            [picking.ship_info_id.ship_from.country_id.name,
             picking.ship_info_id.ship_to.country_id.name,
             picking.ship_info_id.ship_by
             ] if picking.custom_check else [False, False, False]
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this stock '
                                'picking was generated from sale '
                                'order.'))
