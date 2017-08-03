# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.depends('move_ids.state')
    def _compute_is_delayed(self):
        """This function will compute whether related stock moves had been
        done before planned date."""
        for line in self:
            is_delayed = 'None'
            if line.date_planned and line.date_received:
                if line.date_planned > line.date_received:
                    is_delayed = 'True'
                else:
                    is_delayed = 'False'
                line.is_delayed = is_delayed

    @api.multi
    @api.depends('date_order')
    def _compute_year_order(self):
        """This function will compute order year from order date."""
        for line in self:
            year_order = ''
            if line.date_order:
                year_order =\
                    datetime.strptime(line.date_order,
                                      DEFAULT_SERVER_DATETIME_FORMAT
                                      ).date().year
            line.year_order = year_order

    @api.multi
    def _search_year_order(self, operator, value):
        """This function provide the search service based on the order year."""
        if value:
            result = self.search([('date_order', operator, value)])
        return [('id', 'in', result.ids)]

    @api.multi
    def _compute_sale_person(self):
        """This function will compute sale man of related sale order."""
        for line in self:
            sale_person = False
            if line.procurement_ids:
                sale_person = line.procurement_ids.mapped('move_dest_id').\
                    filtered(lambda move: move.state not in ('cancel')).\
                    mapped('procurement_id').mapped('sale_line_id').\
                    mapped('order_id').user_id.id
            line.sale_person = sale_person

    is_delayed = fields.Char(compute='_compute_is_delayed',
                             string='Order Delayed?',
                             store=True, readonly=True,
                             help='Whether related stock moves had been done'
                             ' before planned date?')
    year_order = fields.Char(compute='_compute_year_order',
                             string='Order Year',
                             search='_search_year_order',
                             store=True,
                             help='The field provides filter to each purchase '
                             'order line, and make sure they could be searched'
                             ' by order year')
    sale_person = fields.Many2one(compute='_compute_sale_person',
                                  comodel_name='res.partner',
                                  string='Salesperson',
                                  readonly=True,
                                  help='Sale person of related sale order.')
