# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    partner_name = fields.Char(related='partner_id.name', string='Partner')
    user_group = fields.Boolean(compute='compute_user_group', string="User "
                                                                     "group")

    @api.multi
    def compute_user_group(self):
        for rec in self:
            rec.user_group = self.env.user.has_group(
                'stock_picking_partner_invisible.partner_invisible')
