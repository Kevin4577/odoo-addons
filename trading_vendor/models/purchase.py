# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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

    vendor_product_code = fields.Char(compute='_compute_vendor_product_code',
                                      string='Vendor Product Code',
                                      store=True,
                                      help='The vendor product code could be'
                                      'computed with the specific vendor and'
                                      'product of each purchase order lines.')
