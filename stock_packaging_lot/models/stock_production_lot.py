# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockProductionLot(models.Model):
    "Data model of Stock Production Lot."
    _inherit = "stock.production.lot"

    @api.onchange('gross_by_carton', 'carton_qty')
    def onchange_gross_by_carton(self):
        """To set Gross weight based on Gross by carton and
        Carton qty"""
        self.gross_weight = self.gross_by_carton * self.carton_qty
        return {}

    @api.onchange('net_by_carton', 'carton_qty')
    def onchange_net_by_carton(self):
        """To set Net weight based on Net by carton and
        Carton qty"""
        self.net_weight = self.net_by_carton * self.carton_qty
        return {}

    @api.onchange('qty_per_carton', 'box_per_carton')
    def onchange_qty_per_carton(self):
        """To set Qty per box based on Qty per carton and
        Box per carton"""
        if self.qty_per_carton and self.box_per_carton:
            self.qty_per_box = self.qty_per_carton / (self.box_per_carton or 1)

    carton_no = fields.Char('Carton No')
    carton_qty = fields.Integer('Carton Qty')
    qty_per_carton = fields.Integer('Qty per Carton')
    gross_by_carton = fields.Float('Gross by Carton')
    net_by_carton = fields.Float('Net by Carton')
    box_per_carton = fields.Integer('Box per Carton')
    qty_per_box = fields.Integer('Qty per Box')
    gross_weight = fields.Float('Gross Weight')
    net_weight = fields.Float('Net Weight')
    volume = fields.Float('Volume')
    carton_size = fields.Char('Carton Size')
    shipping_marks = fields.Binary('Shipping Marks')
