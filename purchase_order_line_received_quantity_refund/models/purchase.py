# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.depends('order_id.state', 'move_ids.state',
                 'order_id.picking_ids.state')
    def _compute_qty_received(self):
        """Received quantity of each purchase lines should be computed by
        following expression: received quantity of each purchase lines = total
        received quantity of related stock moves - total refund quantity of
        related stock moves"""
        super(PurchaseOrderLine, self)._compute_qty_received()
        for line in self:
            moves = line.move_ids | line.move_ids.mapped('returned_move_ids')
            total_qty = 0.0
            for move in moves:
                if move.state == 'done':
                    if move.product_uom != line.product_uom and total_qty == 0:
                        total_qty += move.product_uom.\
                            _compute_quantity(move.product_uom_qty,
                                              line.product_uom)
                    elif move.product_uom != line.product_uom:
                        total_qty -= move.product_uom.\
                            _compute_quantity(move.product_uom_qty,
                                              line.product_uom)
                    elif total_qty == 0:
                        total_qty += move.product_uom_qty
                    else:
                        total_qty -= move.product_uom_qty
            line.qty_received = total_qty
