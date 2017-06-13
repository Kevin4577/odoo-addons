# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    """Stock Picking"""
    _inherit = "stock.picking"
    _description = "Stock Picking"

    ship_info_id = fields.Many2one("shipping", 'Shipping Information',
                                   help="Shipping Information")
