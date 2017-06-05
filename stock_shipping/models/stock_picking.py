# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    """Stock Picking"""
    _inherit = "stock.picking"
    _description = "Stock Picking"

    custom_check = fields.Boolean("Custom Check",
                                  help="If this stock picking need to be "
                                       "checked by custom, you could click "
                                       "this check box and make a flag."
                                       "This flag would help other users to "
                                       "know whether this picking order need "
                                       "to be checked by custom. It would "
                                       "just provide the description feature.")
    ship_info_id = fields.Many2one("shipping", 'Shipping Information',
                                   help="Shipping Information")
