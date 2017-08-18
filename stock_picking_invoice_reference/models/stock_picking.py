# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice Reference',
        help='Account Invoice For Related Sale Orders')

    invoice_ids = fields.Many2many(
        "account.invoice",
        'Invoices',
        compute="_get_invoiced",
        readonly=True,
        copy=False)

    @api.multi
    def _get_invoiced(self):
        """
        Get available invoices of related sale order
        :return: 
        """
        for order in self:
            invoice_ids = order.sale_id.invoice_ids
            order.update({
                'invoice_ids': invoice_ids.ids,
            })
