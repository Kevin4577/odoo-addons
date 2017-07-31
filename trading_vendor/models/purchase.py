# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.depends('product_id', 'partner_id')
    def _compute_vendor_product_code(self):
        """This function will compute vendor product code from vendor price
        list, by search with domain of vendor and product of each purchase
        order lines."""
        supplierinfo_obj = self.env['product.supplierinfo']
        for line in self:
            if line.product_id and line.partner_id:
                vendor_product_code = ''
                product_supplierinfo = supplierinfo_obj.\
                    search([('product_id', '=', line.product_id.id),
                            ('name', '=', line.partner_id.id)])
                if product_supplierinfo:
                    vendor_product_code = product_supplierinfo[0].product_code
                line.vendor_product_code = vendor_product_code

    @api.depends('date_order')
    def _compute_month_order(self):
        """This function will compute order month from order date."""
        for line in self:
            month_order = ''
            if line.date_order:
                month_order =\
                    datetime.datetime.strptime(line.date_order,
                                               DEFAULT_SERVER_DATETIME_FORMAT
                                               ).date().month
            line.month_order = month_order

    @api.depends('date_order')
    def _compute_day_order(self):
        """This function will compute order day from order date."""
        for line in self:
            day_order = ''
            if line.date_order:
                day_order =\
                    datetime.datetime.strptime(line.date_order,
                                               DEFAULT_SERVER_DATETIME_FORMAT
                                               ).date().day
            line.day_order = day_order

    @api.depends('move_ids.state')
    def _compute_date_received(self):
        """This function will compute final received date of related
        stock move."""
        for line in self:
            date_received = ''
            for move_id in line.move_ids:
                if move_id.state == "done":
                    date_received = move_id.date
            line.date_received = date_received

    vendor_product_code = fields.Char(
        'Vendor Product Code',
        compute='_compute_vendor_product_code',
        store=True,
        help='The vendor product code could be computed with the specific '
        'vendor and product of each purchase order lines.'
    )

    vendor_reference = fields.Char(
        'Vendor Reference',
        related='order_id.partner_ref',
        readonly=True,
        help='Internal Reference of vendor of purchase order.'
    )

    vendor_order_reference = fields.Char(
        'Vendor Order Reference',
        related='order_id.origin',
        readonly=True,
        help='Source document of vendor order reference of purchase order.'
    )

    purchase_order_reference = fields.Char(
        'Purchase Order Reference',
        related='order_id.name',
        readonly=True,
        help='Order Reference of purchase order.',
    )

    product_reference = fields.Char(
        'Product Reference',
        related='product_id.default_code',
        readonly=True,
        help='Internal Reference of product of purchase order line.'
    )

    customer_product_code = fields.Char(
        'Vendor Product Code',
        related='product_id.customer_product_code',
        readonly=True,
        help='Customer product code of product of purchase order line.'
    )

    date_received = fields.Datetime(
        'Received Date',
        compute='_compute_date_received',
        store=True,
        readonly=True,
        help='Final receive date of stock move.'
    )

    month_order = fields.Char(
        'Order Month',
        compute='_compute_month_order',
        store=True,
        readonly=True,
        help='The order month could be computed from the month of order date.'
    )

    day_order = fields.Char(
        'Order Day',
        compute='_compute_day_order',
        store=True,
        readonly=True,
        help='The order day could be computed from the day of order date.'
    )
