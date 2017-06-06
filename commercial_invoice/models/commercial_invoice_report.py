# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, _
from odoo.exceptions import ValidationError


class CommercialInvoiceReport(models.Model):

    _inherit = 'ir.actions.report.xml'

    @api.model
    def render_report(self, res_ids, name, data):
        action_py3o_report = self.search(
            [("report_name", "=", name),
             ("report_type", "=", "py3o")])
        existed_report = self.env.ref('commercial_invoice.'
                                      'commercial_invoice_report_py3o')
        if action_py3o_report and action_py3o_report.id == existed_report.id:
            base_sale_export_obj = self.env['base.sale.export']
            stock_picking = self.env['stock.picking'].browse(res_ids)
            if stock_picking.sale_id:
                data['so'] = stock_picking.sale_id
                data['sum_qty'], data['sum_amount'], data['product_lines'] =\
                    base_sale_export_obj.\
                    get_product_sale_list(stock_picking.sale_id)
                data['pallet_sum'], gross_weight, net_weight, volume,\
                    package_list =\
                    base_sale_export_obj.\
                    get_product_stock_list(stock_picking)
            else:
                raise ValidationError(_('Please check whether this stock '
                                        'picking was generated from sale'
                                        ' order.'))
        return super(CommercialInvoiceReport, self).render_report(
            res_ids, name, data)
