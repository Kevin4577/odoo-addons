# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.depends('purchase_line_id.procurement_ids.move_dest_id.state')
    def _compute_state_sale(self):
        """This function will compute state from the stock move of
        related sale order."""
        for line in self:
            if line.purchase_line_id:
                if line.purchase_line_id.procurement_ids:
                    if line.purchase_line_id.procurement_ids.move_dest_id.\
                            state == 'done':
                        line.state_sale = 'done'
                    else:
                        line.state_sale = 'waiting'
                else:
                    line.state_sale = ''

    vendor_reference = fields.Char(
        'Vendor Reference',
        related='purchase_line_id.vendor_reference',
        readonly=True,
        help='Internal Reference of vendor of purchase order.'
    )

    vendor_order = fields.Char(
        'Order Vendor',
        related='purchase_line_id.partner_id.name',
        readonly=True,
        help='Name of vendor of purchase order.'
    )

    customer_reference = fields.Char(
        'Customer Reference',
        related='purchase_line_id.order_id.partner_id.ref',
        readonly=True,
        help='Internal Reference of customer of purchase order.'
    )

    vendor_order_reference = fields.Char(
        'Vendor Order Reference',
        related='purchase_line_id.vendor_order_reference',
        readonly=True,
        help='Source document of vendor order reference of purchase order.'
    )

    purchase_order_reference = fields.Char(
        'Purchase Order Reference',
        related='purchase_line_id.purchase_order_reference',
        readonly=True,
        help='The purchase order number of related purchase order.'
    )

    customer_product_code = fields.Char(
        'Customer Product Code',
        related='product_id.customer_product_code',
        readonly=True,
        help='The customer product code of specific product.'
    )

    qty_order = fields.Float(
        'Order Quantity',
        related='purchase_line_id.product_qty',
        readonly=True,
        help='The original product quantity of related purchase order line.'
    )

    price_subtotal_order = fields.Monetary(
        'Total Price Order',
        related='purchase_line_id.price_subtotal',
        readonly=True,
        help='The total amount of related purchase order line.'
    )

    state_sale = fields.Char(
        'Sale Order State',
        compute='_compute_state_sale',
        readonly=True,
        store=True,
        help='The state of stock move of related sale order.'
    )

    hs_cn_name = fields.Char(
        'Product HS Code CN Name',
        related='product_id.hs_cn_name',
        readonly=True,
        help='The state of stock move of related sale order.'
    )
