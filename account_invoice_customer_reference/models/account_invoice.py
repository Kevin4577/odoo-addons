# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    internal_reference = fields.Char(
        'Internal Reference',
        help='Customer Invoice Internal Reference'
    )
