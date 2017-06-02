# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPackaging(models.Model):
    """Product Packaging"""
    _inherit = "product.packaging"

    weight = fields.Float("Weight (KG)")
    volume = fields.Float("Volume (CBM)")
