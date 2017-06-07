# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, _
from odoo.exceptions import ValidationError


class SaleExportCustomsDeclarationItemsPrintout(models.Model):
    _inherit = "ir.actions.report.xml"

    @api.model
    def render_report(self, res_ids, name, data):
        """This function would get customs declaration items of the
        specific stock picking(s), in order to render the ods template."""
        action_py3o_report = self.search(
            [("report_name", "=", name), ("report_type", "=", "py3o")])
        existed_report =\
            self.env.ref('sale_export_customs_declaration_items_printout.'
                         'sale_export_customs_declaration_items_printout_py3o')
        if action_py3o_report and action_py3o_report.id == existed_report.id:
            base_sale_report_obj = self.env['base.sale.export']
            picking_id = self.env['stock.picking'].browse(res_ids)
            if picking_id and picking_id.sale_id:
                data['hs_lines'] = base_sale_report_obj.\
                    get_product_hs_code_list(picking_id.sale_id)
            else:
                raise ValidationError(_('Please check whether this stock'
                                        'picking was generated'
                                        'from sale order.'))
        return super(SaleExportCustomsDeclarationItemsPrintout, self).\
            render_report(res_ids, name, data)
