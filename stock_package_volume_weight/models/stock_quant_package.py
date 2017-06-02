# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    """Stock Quant Package"""
    _inherit = "stock.quant.package"

    weight = fields.Float("Weight (KG)")
    carton_qty = fields.Float("Volume (CBM)")

    @api.onchange('packaging_id')
    def _onchange_packaging_id(self):
        """Will catch the packaging related values if change with default
        values for weight and volume."""
        self.weight = self.packaging_id.weight
        self.carton_qty = self.packaging_id.carton_qty
