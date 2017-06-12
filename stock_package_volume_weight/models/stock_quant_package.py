# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    """Stock Quant Package"""
    _inherit = "stock.quant.package"

    weight = fields.Float("Weight (KG)")
    volume = fields.Float("Volume (CBM)")
    forwarder_no = fields.Char("Forwarder No")

    @api.onchange('packaging_id')
    def _onchange_packaging_id(self):
        """Will catch the packaging related values if change with default
        values for weight and volume."""
        if self.packaging_id:
            self.weight = self.packaging_id.weight
            self.volume = self.packaging_id.volume
