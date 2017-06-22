# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """Sales Order"""
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        """
        action_confirm method will check whether customer and product has or
        not internal reference number.
        """
        so_cnt = self.search_count([('id', 'in', self.ids),
                                    ('partner_id.ref', '=', False)])
        if so_cnt > 0:
            raise ValidationError("Customer needs to have "
                                  "Internal Reference before a sales "
                                  "quotation could be confirmed")
        sol_cnt = self.env['sale.order.line'].\
            search_count([('order_id', 'in', self.ids),
                          ('product_id.default_code', '=', False)])
        if sol_cnt > 0:
            raise ValidationError("Products need to have "
                                  "Internal Reference before a sales "
                                  "quotation could be confirmed")
        return super(SaleOrder, self).action_confirm()
