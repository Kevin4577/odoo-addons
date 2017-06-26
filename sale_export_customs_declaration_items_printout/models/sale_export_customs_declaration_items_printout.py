# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.exceptions import ValidationError
from odoo.addons.report_py3o.models import py3o_report


@py3o_report.py3o_report_extender(
    report_xml_id='sale_export_customs_declaration_items_printout.'
    'sale_export_customs_declaration_items_printout_py3o')
def change_ctx(report_xml_id, ctx):
    data = {}
    """This function would get customs declaration items of the
       specific stock picking(s), in order to render the ods template."""
    picking_id = ctx['objects']
    trading_sale_obj = picking_id.env['trading.sale']
    if picking_id and picking_id.sale_id:
        data['hs_lines'] = trading_sale_obj.\
            get_product_hs_code_list(picking_id.sale_id)
        ctx['data'].update(data)
    else:
        raise ValidationError(_('Please check whether this stock'
                                'picking was generated'
                                'from sale order.'))
