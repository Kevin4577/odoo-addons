# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def name_get(self):
        """
            Add invoice reference into the display name
        :return:
        """
        res = super(AccountInvoice, self).name_get()
        result = []
        for inv in res:
            current_invoice = self.browse(inv[0])
            result.append(
                (
                    inv[0],
                    '(%s) %s' % (
                        current_invoice.internal_reference or '',
                        inv[1]
                    )
                )
            )
        return result
