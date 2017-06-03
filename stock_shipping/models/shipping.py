# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class Shipping(models.Model):
    """Shipping """
    _name = "shipping"
    _description = "Shipping Management"

    name = fields.Char('Name', help='Name of shipping detail')
    ship_from = fields.Many2one('res.partner', 'Ship From',
                                help='Source shipping location', index=True)
    ship_to = fields.Many2one('res.partner', 'Ship To',
                              help='Destination shipping location', index=True)
    ship_by = fields.Char("Shipping Type", help="Shipping Type")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "The name must be unique !"),
    ]

    @api.multi
    def name_get(self):
        return [(shipping.id, "(%s) %s-%s By %s" % (shipping.name,
                                                    shipping.ship_from.name,
                                                    shipping.ship_to.name,
                                                    shipping.ship_by
                                                    )) for shipping in self]
