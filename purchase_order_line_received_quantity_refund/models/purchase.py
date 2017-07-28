# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    qty_received_returned =\
        fields.Float(compute='_compute_qty_received_returned',
                     string="Received Qty Returned",
                     digits=dp.get_precision('Product Unit of Measure'),
                     store=False)

    @api.multi
    def _compute_qty_received_returned(self):
        for line in self:
            if line.order_id.state not in ['purchase', 'done']:
                line.qty_received = 0.0
                continue
            if line.product_id.type not in ['consu', 'product']:
                line.qty_received = line.product_qty
                continue
            total = 0.0
            for move in line.move_ids:
                if move.state == 'done':
                    if move.product_uom != line.product_uom:
                        total += move.product_uom.\
                            _compute_quantity(move.product_uom_qty,
                                              line.product_uom)
                    else:
                        total += move.product_uom_qty
            total_reduce = 0.0
            for move in line.move_ids.mapped('returned_move_ids'):
                if move.state == 'done':
                    if move.product_uom != line.product_uom:
                        total_reduce += move.product_uom._compute_quantity(
                            move.product_uom_qty, line.product_uom)
                    else:
                        total_reduce += move.product_uom_qty
            line.qty_received_returned = total_reduce
            line.write({
                'qty_received': total - total_reduce
            })
