# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class StockPicking(models.Model):
    "Data model of Stock Picking."
    _inherit = "stock.picking"

    def _create_lots_for_picking(self):
        """This function should be inherited, and make sure each lots of
        incoming order had been created by the original method.
        Then input the additional lot information into the specific lot
        from stock operation line."""
        res = super(StockPicking, self)._create_lots_for_picking()
        for pack_operation_lot in self.mapped('pack_operation_ids').\
                mapped('pack_lot_ids'):
            if pack_operation_lot.lot_id:
                lot = pack_operation_lot.lot_id
                lot.write({
                    'carton_no': pack_operation_lot.carton_no,
                    'carton_qty': pack_operation_lot.carton_qty,
                    'qty_per_carton': pack_operation_lot.qty_per_carton,
                    'gross_by_carton': pack_operation_lot.gross_by_carton,
                    'net_by_carton': pack_operation_lot.net_by_carton,
                    'volume_by_carton': pack_operation_lot.volume_by_carton,
                    'box_per_carton': pack_operation_lot.box_per_carton,
                    'qty_per_box': pack_operation_lot.qty_per_box,
                    'gross_weight': pack_operation_lot.gross_weight,
                    'net_weight': pack_operation_lot.net_weight,
                    'volume': pack_operation_lot.volume,
                    'carton_size': pack_operation_lot.carton_size,
                    'shipping_mark': pack_operation_lot.shipping_mark,
                    'mix_loading': pack_operation_lot.mix_loading})
        return res

    def _prepare_pack_ops(self, quants, forced_qties):
        """This function should be inherited, and make sure each available
        lots of incoming order had been prepared for each stock operation
        lines. Then input the additional lot information from specific lot
        to each stock operation lines."""
        res = super(StockPicking, self)._prepare_pack_ops(quants, forced_qties)
        for pack_operation_value in res:
            for pack_lot_value in pack_operation_value.get(
                    'pack_lot_ids', []):
                for element in pack_lot_value:
                    if isinstance(element, dict) and element['lot_id']:
                        lot = self.env['stock.production.lot'].\
                            browse(element['lot_id'])
                        element.update({
                            'carton_no': lot.carton_no,
                            'carton_qty': lot.carton_qty,
                            'qty_per_carton': lot.qty_per_carton,
                            'gross_by_carton': lot.gross_by_carton,
                            'net_by_carton': lot.net_by_carton,
                            'volume_by_carton': lot.volume_by_carton,
                            'box_per_carton': lot.box_per_carton,
                            'qty_per_box': lot.qty_per_box,
                            'gross_weight': lot.gross_weight,
                            'net_weight': lot.net_weight,
                            'volume': lot.volume,
                            'carton_size': lot.carton_size,
                            'shipping_mark': lot.shipping_mark,
                            'mix_loading': lot.mix_loading})
        return res
