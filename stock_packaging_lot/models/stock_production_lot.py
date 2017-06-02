# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockProductionLot(models.Model):
    "Data model of Stock Production Lot."
    _inherit = "stock.production.lot"

    @api.depends('qty_per_carton', 'box_per_carton')
    def _compute_qty_per_box(self):
        """To compute Qty per box based on Qty per carton and
        Box per carton"""
        self.qty_per_box = self.qty_per_carton / (self.box_per_carton or 1)

    @api.depends('gross_by_carton', 'carton_qty')
    def _compute_gross_weight(self):
        """To compute Gross weight based on Gross by carton and
        Carton qty"""
        self.gross_weight = self.gross_by_carton * self.carton_qty

    @api.depends('net_by_carton', 'carton_qty')
    def _compute_net_weight(self):
        """To compute Net weight based on Net by carton and
        Carton qty"""
        self.net_weight = self.net_by_carton * self.carton_qty

    carton_no = fields.Char('Carton No')
    carton_qty = fields.Integer('Carton Qty')
    qty_per_carton = fields.Integer('Qty per Carton')
    gross_by_carton = fields.Float('Gross by Carton')
    net_by_carton = fields.Float('Net by Carton')
    box_per_carton = fields.Integer('Box per Carton')
    qty_per_box = fields.Integer(compute=_compute_qty_per_box,
                                 string='Qty per Box')
    gross_weight = fields.Float(compute=_compute_gross_weight,
                                string='Gross Weight')
    net_weight = fields.Float(compute=_compute_net_weight,
                              string='Net Weight')
    volume = fields.Float('Volume')
    carton_size = fields.Char('Carton Size')
    shipping_marks = fields.Binary('Shipping Marks')
