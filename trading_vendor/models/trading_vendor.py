# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class TradingVendor(models.Model):

    _name = 'trading.vendor'

    @api.multi
    def get_partner_contact(self, partner):
        """This function return the contact person information of partner."""
        if partner.child_ids:
            contact_name = partner.child_ids[0].name
            contact_email = partner.child_ids[0].email
            return contact_name, contact_email

    @api.multi
    def get_purchase_order_vendor_contact(self, purchase_order):
        """This function return the contact person information of vendor
        of purchase order."""
        if purchase_order.partner_id:
            contact_name, contact_email =\
                self.get_partner_contact(purchase_order.partner_id)
            return {'vendor_contact_name': contact_name,
                    'vendor_contact_email': contact_email}

    @api.multi
    def get_purchase_order_company_contact(self, purchase_order):
        """This function return the contact person information of company
        of purchase order."""
        if purchase_order.company_id:
            contact_name, contact_email =\
                self.get_partner_contact(purchase_order.company_id)
            return {'company_contact_name': contact_name,
                    'company_contact_email': contact_email}

    @api.multi
    def get_purchase_order_total_quantity_and_price(self, purchase_order):
        """This function return the total quantity and total price of
        purchase order."""
        total_quantity = sum([po_line.product_qty for po_line in
                                             purchase_order.order_line])
        total_price = sum([po_line.price_total for po_line in
                                             purchase_order.order_line])
        return total_quantity, total_price

    def get_purchase_order_list_total_quantity_and_price(self,
                                                         purchase_order_list):
        """This function return the total quantity and total price of
        purchase order list."""
        total_quantity = 0.0
        total_price = 0.0
        for order in purchase_order_list:
            subtotal_quantity, subtotal_price =\
                self.get_purchase_order_total_quantity_and_price(order)
            total_quantity += subtotal_quantity
            total_price += subtotal_price
        return total_quantity, total_price
