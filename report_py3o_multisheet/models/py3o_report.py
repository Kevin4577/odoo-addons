# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class Py3oReport(models.TransientModel):
    _inherit = 'py3o.report'
    _description = """ Overwrite the create_single_report method, in order to
                   modify the template file of py3o report with multiple sheets
                   before this template file was used to render with local
                   context """

    @api.multi
    def _create_single_report(self, model_instance, data, save_in_attachment):
        """ This function to modify the template file, then generate our py3o
        report"""
        self._get_parser_context(model_instance, data)
        res = super(Py3oReport, self)._create_single_report(
            model_instance,
            data,
            save_in_attachment)
        return res
