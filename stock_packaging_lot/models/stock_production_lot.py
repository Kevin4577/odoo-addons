# -*- coding: utf-8 -*-
# © 2017 Elico corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


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
        qty_per_box = 0
        if self.qty_per_carton and self.box_per_carton:
            qty_per_box = self.qty_per_carton / (self.box_per_carton or 1)
        self.qty_per_box = qty_per_box
        return {}

    @api.onchange('volume_by_carton', 'carton_qty')
    def onchange_volume_by_carton(self):
        """To set volume based on Volume by carton and
        Carton qty"""
        self.volume = self.volume_by_carton * self.carton_qty
        return {}

    carton_no = fields.Char('Carton No')
    carton_qty = fields.Float(
        'Carton Qty',
        digits=dp.get_precision('Case Quantity'))
    qty_per_carton = fields.Float(
        'Qty per Carton',
        digits=dp.get_precision('Case Quantity'))
    gross_by_carton = fields.Float(
        'Gross by Carton',
        digits=dp.get_precision('Case Weight'))
    volume_by_carton = fields.Float(
        'Volume by carton',
        digits=dp.get_precision('Case Volume'))
    net_by_carton = fields.Float(
        'Net by Carton',
        digits=dp.get_precision('Case Weight'))
    box_per_carton = fields.Float(
        'Box per Carton',
        digits=dp.get_precision('Case Quantity'))
    qty_per_box = fields.Float(
        'Qty per Box',
        digits=dp.get_precision('Case Quantity'))
    gross_weight = fields.Float(
        'Gross Weight',
        digits=dp.get_precision('Case Weight'))
    net_weight = fields.Float(
        'Net Weight',
        digits=dp.get_precision('Case Weight'))
    volume = fields.Float(
        'Volume',
        digits=dp.get_precision('Case Volume'))
    carton_size = fields.Char('Carton Size')
    shipping_mark = fields.Text('Shipping Marks')
    mixed_loading = fields.Boolean('Mixed Loading?')


class StockPackOperationLot(models.Model):
    "Data model of Stock Pack Operation Lot."
    _inherit = "stock.pack.operation.lot"

    @api.onchange('qty_per_carton', 'box_per_carton')
    def onchange_qty_per_carton(self):
        """To set Qty per box based on Qty per carton and
        Box per carton"""
        qty_per_box = 0
        if self.qty_per_carton and self.box_per_carton:
            qty_per_box = self.qty_per_carton / (self.box_per_carton or 1)
        self.qty_per_box = qty_per_box
        return {}

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

    @api.onchange('volume_by_carton', 'carton_qty')
    def onchange_volume_by_carton(self):
        """To set volume based on Volume by carton and
        Carton qty"""
        self.volume = self.volume_by_carton * self.carton_qty
        return {}

    @api.onchange('qty_per_carton', 'carton_qty')
    def onchange_qty_per_carton_carton_qty(self):
        """To set volume based on Volume by carton and
        Carton qty"""
        self.qty = self.qty_per_carton * self.carton_qty
        return {}

    carton_no = fields.Char('Carton No')
    carton_qty = fields.Float(
        'Carton Qty',
        digits=dp.get_precision('Case Quantity'))
    qty_per_carton = fields.Float(
        'Qty per Carton',
        digits=dp.get_precision('Case Quantity'))
    gross_by_carton = fields.Float(
        'Gross by Carton',
        digits=dp.get_precision('Case Weight'))
    volume_by_carton = fields.Float(
        'Volume by carton',
        digits=dp.get_precision('Case Volume'))
    net_by_carton = fields.Float(
        'Net by Carton',
        digits=dp.get_precision('Case Weight'))
    box_per_carton = fields.Float(
        'Box per Carton',
        digits=dp.get_precision('Case Quantity'))
    qty_per_box = fields.Float(
        'Qty per Box',
        digits=dp.get_precision('Case Quantity'))
    gross_weight = fields.Float(
        'Gross Weight',
        digits=dp.get_precision('Case Weight'))
    net_weight = fields.Float(
        'Net Weight',
        digits=dp.get_precision('Case Weight'))
    volume = fields.Float(
        'Volume',
        digits=dp.get_precision('Case Volume'))
    carton_size = fields.Char('Carton Size')
    shipping_mark = fields.Text('Shipping Marks')
    mixed_loading = fields.Boolean('Mixed Loading?')

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        """This function allow user to select the available lot to input the
        additional lot information into operation lines."""
        if self.lot_id:
            self.carton_no = self.lot_id.carton_no
            self.carton_qty = self.lot_id.carton_qty
            self.qty_per_carton = self.lot_id.qty_per_carton
            self.gross_by_carton = self.lot_id.gross_by_carton
            self.net_by_carton = self.lot_id.net_by_carton
            self.volume_by_carton = self.lot_id.volume_by_carton
            self.box_per_carton = self.lot_id.box_per_carton
            self.qty_per_box = self.lot_id.qty_per_box
            self.gross_weight = self.lot_id.gross_weight
            self.net_weight = self.lot_id.net_weight
            self.volume = self.lot_id.volume
            self.carton_size = self.lot_id.carton_size
            self.shipping_mark = self.lot_id.shipping_mark
            self.mixed_loading = self.lot_id.mixed_loading
        return {}
