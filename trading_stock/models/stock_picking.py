# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    """Stock Picking"""
    _inherit = "stock.picking"
    _description = "Stock Picking"

    custom_check = fields.Boolean("Custom Check",
                                  help="Mark this if customs need to check"
                                       "the stock picking")
