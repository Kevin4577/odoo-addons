# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('procurement_ids.move_dest_id.state')
    def _compute_qty_delivered(self):
        """This function will compute delivery quantity of related
        sale order."""
        for line in self:
            qty_delivery = False
            if line.procurement_ids:
                qty_delivery =\
                    sum(line.procurement_ids.mapped('move_dest_id').
                        filtered(lambda move: move.state not in ('cancel')).
                        mapped('procurement_id').mapped('sale_line_id').
                        mapped('product_uom_qty'))
            line.qty_delivered = qty_delivery

    @api.depends('procurement_ids.move_dest_id.state')
    def _compute_qty_canceled(self):
        """This function will compute canceled quantity of related
        stock move."""
        for line in self:
            qty_canceled = False
            if line.procurement_ids:
                qty_canceled =\
                    sum(line.procurement_ids.mapped('move_dest_id').
                        filtered(lambda move: move.state in ('cancel')).
                        mapped('product_qty'))
            line.qty_canceled = qty_canceled

    def _compute_date_sale(self):
        """This function will compute order date of related sale order."""
        for line in self:
            date_sale = False
            if line.procurement_ids:
                date_sale = line.procurement_ids.mapped('move_dest_id').\
                    filtered(lambda move: move.state not in ('cancel')).\
                    mapped('procurement_id').mapped('sale_line_id').\
                    mapped('order_id').mapped('date_order')
            line.date_sale = date_sale

    @api.depends('currency_id', 'price_subtotal')
    def _compute_price_subtotal_company(self):
        """This function will compute order date of related sale order."""
        for line in self:
            price_subtotal_company = False
            if line.currency_id:
                currency_company = self.env['res.currency'].\
                    search([('name', '=', line.currency_id.name)])
                price_subtotal_company =\
                    self.env['res.currency']._compute(line.currency_id,
                                                      currency_company,
                                                      line.price_subtotal)
            line.price_subtotal_company = price_subtotal_company

    qty_delivered = fields.Float(
        'Delivery Quantity',
        compute='_compute_qty_delivered',
        readonly=True,
        store=True,
        help='Delivery Quantity of related sale order.',
    )

    qty_canceled = fields.Float(
        'Canceled Quantity',
        compute='_compute_qty_canceled',
        readonly=True,
        store=True,
        help='''Canceled quantity of product during the stock move of
            related sale order.''',
    )

    date_sale = fields.Datetime(
        'Sale Date',
        compute='_compute_date_sale',
        readonly=True,
        help='Order Date of related sale order.'
    )

    price_subtotal_company = fields.Monetary(
        'Total Price Company',
        compute='_compute_price_subtotal_company',
        readonly=True,
        store=True,
        help='Total price converted to the current company currency.',
    )

    currency_rate = fields.Float(
        'Currency Rate',
        related='currency_id.rate',
        readonly=True,
        help='Currency Rate between other currency and company currency .',
    )
