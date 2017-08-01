# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    returned_purchase_id = fields.Many2one(
        string='Return Purchase Order',
        comodel='purchase.order',
        related='move_lines.origin_returned_move_id.purchase_line_id.order_id',
        readonly=True,
        store=True,
        help='The related purchase order of current return stock picking order'
    )
