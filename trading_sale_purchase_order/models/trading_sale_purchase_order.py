# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, _
import datetime
from openerp.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TradingSalePurchaseOrder(models.Model):
    _inherit = "ir.actions.report.xml"

    @api.model
    def render_report(self, res_ids, name, data):
        """This function would gain the invoice, address and other data from
        sale order of specific stock picking, and sum the product quantity
        and price group by same hs code, in order to render the ods template
        with necessary data. """
        action_py3o_report = self.search([("report_name", "=", name),
                                          ("report_type", "=", "py3o")])
        existed_report =\
            self.env.ref('trading_sale_purchase_order.'
                         'trading_sale_purchase_order_py3o')
        if action_py3o_report and action_py3o_report.id == existed_report.id:
            trading_sale_obj = self.env['trading.sale']
            picking = self.env['stock.picking'].browse(res_ids)
            if picking.sale_id:
                data['so'] = picking.sale_id
                data['sum_qty'], data['sum_amount'], data['product_lines'] =\
                    trading_sale_obj.get_product_sale_list(picking.sale_id)
                data['date'] = datetime.datetime.\
                    strptime(picking.min_date, DEFAULT_SERVER_DATETIME_FORMAT
                             ) - relativedelta(days=30)
            else:
                raise ValidationError(_('Please check whether this stock '
                                        'picking was generated from sale '
                                        'order.'))
        return super(TradingSalePurchaseOrder, self).\
            render_report(res_ids, name, data)
