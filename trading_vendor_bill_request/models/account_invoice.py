# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'account.invoice'

    def _compute_qty_total(self):
        """This function will compute sum of product quantity of each invoice
        lines. The total quantity of product in account invoice should be
        computed anytime without being stored in database."""
        for line in self.invoice_line_ids:
            self.qty_total += line.quantity

    qty_total = fields.Float(
        'Product Total Quantity',
        compute='_compute_qty_total',
        help='The product total quantity could be computed from the sum of '
        'product quantity of each invoice lines.'
    )
