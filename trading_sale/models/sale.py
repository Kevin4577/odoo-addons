# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    """Data model of Sale Order."""
    _inherit = 'sale.order'

    @api.depends('invoice_ids.residual')
    def _compute_payment_rate(self):
        """This function calculate payment rate with the paid amount of all
        invoices related to this order, and the total amount of them."""
        for rec in self:
            sum_residual = sum([invoice.residual for
                                invoice in rec.invoice_ids])
            sum_amount = sum([invoice.amount_total for
                              invoice in rec.invoice_ids])
            if sum_amount > 0:
                rec.payment_rate = sum_residual / sum_amount
            else:
                rec.payment_rate = 0

    payment_rate = fields.Float(compute='_compute_payment_rate',
                                string='Payment Rate',
                                store=True, readonly=True,
                                help='The payment rate of sale order should be'
                                ' calculated with the paid amount of all'
                                ' invoices related to this order, and the'
                                ' total amount of them. The expression should'
                                ' be: payment rate = sum(paid amount of '
                                'invoice) / sum(total amount of invoice)')


class SaleOrderLine(models.Model):
    """Data model of Sale Order line."""
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('write_date')
    def _compute_last_update_year(self):
        """This function computes the last update year of each
        sale order lines."""
        for line in self:
            write_date = datetime.datetime.\
                strptime(line.write_date, DEFAULT_SERVER_DATETIME_FORMAT).\
                date()
            self.last_update_year = write_date.year

    @api.multi
    def _search_last_update_year(self, operator, value):
        """This function provide the search service based on the last
        update year."""
        if value:
            result = self.search([('write_date', operator, value)])
        return [('id', 'in', result.ids)]

    @api.depends('product_id.product_stage_id', 'product_id.product_line_id',
                 'product_id.product_class_id', 'product_id.product_family_id')
    def _compute_product_class(self):
        """This function computes the product class field with combination
        of product classes of product."""
        for line in self:
            product_class = ''
            if line.product_id.product_stage_id\
                and line.product_id.product_line_id and\
                    line.product_id.product_class_id and\
                    line.product_id.product_family_id:
                product_class = line.product_id.product_stage_id.cn_name\
                    + '-' + line.product_id.product_line_id.cn_name + '-' +\
                    line.product_id.product_class_id.cn_name + '-' +\
                    line.product_id.product_family_id.cn_name
            line.update({'product_class': product_class})

    @api.depends('qty_delivered', 'discount', 'price_unit')
    def _compute_delivery_amount(self):
        """This function calculate delivery amount of each sale order lines."""
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_delivery = line.qty_delivered * price
            line.update({'price_delivery': price_delivery})

    @api.depends('qty_delivered', 'product_uom_qty')
    def _compute_qty_to_delivery(self):
        """This function calculate to-delivery quantity of each sale order
        lines."""
        for line in self:
            qty_to_delivery = line.product_uom_qty - line.qty_delivered
            line.update({'qty_to_delivery': qty_to_delivery})

    @api.depends('qty_to_delivery', 'discount', 'price_unit')
    def _compute_price_to_delivery(self):
        """This function calculate to-delivery quantity of each sale order
        lines."""
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_to_delivery = line.qty_to_delivery * price
            line.update({'price_to_delivery': price_to_delivery})

    @api.depends('qty_to_invoice', 'discount', 'price_unit')
    def _compute_price_to_invoice(self):
        """This function calculate to-delivery quantity of each sale order
        lines."""
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_to_invoice = line.qty_to_invoice * price
            line.update({'price_to_invoice': price_to_invoice})

    @api.depends('qty_invoiced', 'discount', 'price_unit')
    def _compute_price_invoiced(self):
        """This function calculate to-delivery quantity of each sale order
        lines."""
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_invoiced = line.qty_invoiced * price
            line.update({'price_invoiced': price_invoiced})

    @api.depends('order_id.payment_rate', 'price_invoiced')
    def _compute_price_to_payment(self):
        """This function calculate to-pay amount of each sale order lines."""
        for line in self:
            line.update({'price_to_payment': line.price_invoiced *
                         (1 - line.order_id.payment_rate)})

    @api.depends('order_id.payment_rate', 'price_invoiced')
    def _compute_price_payment(self):
        """This function calculate paid amount of each sale order lines."""
        for line in self:
            line.update({'price_payment': line.price_invoiced *
                         line.order_id.payment_rate})

    last_update_year = fields.Char(compute='_compute_last_update_year',
                                   string='Last Update Year',
                                   search='_search_last_update_year',
                                   help='The field provides filter to each'
                                   ' sale order line, and make sure they'
                                   ' could be searched by last update year.')
    customer_reference = fields.Char(related='order_partner_id.ref',
                                     string='Customer Reference',
                                     readonly=True, help='Internal reference '
                                     'of customer of related sale order.')
    customer_order_reference = fields.Char(related='order_id.client_order_ref',
                                           string='Customer Order Reference',
                                           readonly=True,
                                           help='Customer order reference of'
                                           ' related sale order.')
    sale_order_reference = fields.Char(related='order_id.name',
                                       string='Sale Order Reference',
                                       readonly=True,
                                       help='Sale order reference of related'
                                       ' sale order.')
    product_reference = fields.Char(related='product_id.default_code',
                                    string='Product Reference',
                                    readonly=True,
                                    help='Internal reference of related'
                                    ' product.')
    product_class = fields.Char(compute='_compute_product_class',
                                string='Product Class',
                                store=True, readonly=True,
                                help='Combination of name of product classes.')
    price_delivery = fields.Monetary(compute='_compute_delivery_amount',
                                     string='Amount Delivered',
                                     store=True, readonly=True,
                                     help='The total amount of delivery '
                                     'quantity of product. The expression'
                                     ' should be: delivery amount = product'
                                     'delivery quantity * unit price of'
                                     ' product.')
    qty_to_delivery = fields.Float(compute='_compute_qty_to_delivery',
                                   string='Quantity to Delivered',
                                   store=True, readonly=True,
                                   digits=dp.get_precision('Product Unit of '
                                                           'Measure'),
                                   help='The to-delivery quantity of product.'
                                   'The expression should be: to delivery '
                                   'quantity = product quantity - delivered '
                                   'quantity')
    price_to_delivery = fields.Monetary(compute='_compute_price_to_delivery',
                                        string='Amount to Delivered',
                                        store=True, readonly=True,
                                        help='The to-delivery amount of '
                                        'product. The expression should be: '
                                        'to delivery amount = unit price of'
                                        ' product * to delivery quantity')
    price_to_invoice = fields.Monetary(compute='_compute_price_to_invoice',
                                       string='Amount to Invoice',
                                       store=True, readonly=True,
                                       help='The to-invoice amount of product.'
                                       ' The expression should be: to invoice'
                                       ' amount = unit price of product * to'
                                       ' invoice quantity.')
    price_invoiced = fields.Monetary(compute='_compute_price_invoiced',
                                     string='Amount Invoiced',
                                     store=True, readonly=True,
                                     help='The to-invoice amount of product.'
                                     ' The expression should be: invoiced'
                                     ' amount = unit price of product *'
                                     ' invoiced quantity')
    price_to_payment = fields.Monetary(compute='_compute_price_to_payment',
                                       string='Amount to Pay',
                                       store=True, readonly=True,
                                       help='The amount of product plan to be'
                                       ' paid. The expression should be: to '
                                       'payment amount = invoiced amount * '
                                       '(1 - payment rate)')
    price_payment = fields.Monetary(compute='_compute_price_payment',
                                    string='Amount Paid',
                                    store=True, readonly=True,
                                    help='The amount of product already be '
                                    'paid. The expression should be: payment '
                                    'amount = invoiced amount * payment rate')
