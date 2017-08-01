# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class StockMove(models.Model):
    """Stock Move"""
    inherit = "stock.move"
    _description = "Stock Move"

    date_order = fields.Datetime(related='purchase_line_id.order_id.'
                                 'date_order',
                                 string='Date Order',
                                 readonly=True, help='The order date of '
                                 'related purchase order.')
    customer_reference = fields.Char(related='purchase_line_id.order_id.'
                                     'partner_ref',
                                     string='Customer Reference',
                                     readonly=True,
                                     help='The internal reference of vendor '
                                     'for related purchase order.')
    customer_order_reference = fields.Char(related='purchase_line_id.order_id.'
                                           'origin',
                                           string='Customer Order Number',
                                           readonly=True,
                                           help='The customer order number of '
                                           'related purchase order.')
    purchase_order_number = fields.Char(related='purchase_line_id.order_id.'
                                        'name',
                                        string='Purchase Order Number',
                                        readonly=True,
                                        help='The purchase order number of '
                                        'related purchase order.')
    product_reference = fields.Char(related='product_id.default_code',
                                    string='Product Reference',
                                    readonly=True,
                                    help='The internal reference of specific '
                                    'product.')
    customer_product_code = fields.Char(related='product_id.'
                                        'customer_product_code',
                                        string='Customer Product Code',
                                        readonly=True,
                                        help='The customer product code of '
                                        'specific product.')
    qty_order = fields.Float(related='purchase_line_id.product_qty',
                             string='Order Quantity',
                             readonly=True,
                             digits=dp.get_precision('Product Unit of '
                                                     'Measure'),
                             help='The original product quantity of'
                             ' related purchase order line.')
    qty_received = fields.Float(related='purchase_line_id.qty_received',
                                string='Actual Received Quantity',
                                readonly=True,
                                digits=dp.get_precision('Product Unit of '
                                                        'Measure'),
                                help='The actual received product quantity of'
                                ' related purchase order line.')
