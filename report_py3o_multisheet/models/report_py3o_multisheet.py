# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from ezodf import opendoc
import math
import copy


class IrActionsReportXml(models.Model):
    _inherit = 'ir.actions.report.xml'

    py3o_template_fallback_base = fields.\
        Char(size=128, help='If the user does not provide a template'
             ' this one will be used.')


class ReportPy3oMultisheet(models.Model):
    "Report Py3o Multisheet"
    _name = 'report.py3o.multisheet'
    _description = 'Report Py3o Multisheet'

    @api.model
    def create_new_template(self, head_end_line, lines_per_sheet,
                            total_line_num, attribute_num_per_line,
                            attribute_per_line, template_new_path,
                            template_base_path):
        """This function would generate the new template from base one. It
        would duplicate the head and footer of first sheet into new sheets,
        and make the body could be customized by user."""
        lines_per_line =\
            int(math.ceil(len(attribute_per_line
                              ) / float(attribute_num_per_line)))
        add_sheet_num = int(math.floor(total_line_num / lines_per_sheet))
        doc = opendoc(template_base_path)
        sheets = doc.sheets
        sheet = sheets[0]
        for index in range(add_sheet_num):
            sheet_new = copy.deepcopy(sheet)
            sheets.append(sheet_new)
        for index1, sheet in enumerate(sheets):
            sheet.insert_rows(index=head_end_line,
                              count=lines_per_sheet * lines_per_line)
            for row in range(0, lines_per_sheet * lines_per_line,
                             lines_per_line):
                for index2, attr in enumerate(attribute_per_line):
                    if (index1 * lines_per_sheet + row /
                            lines_per_line < total_line_num):
                        if index2 < 4 or 5 < index2 < 9:
                            sheet[row + head_end_line, index2].set_value((
                                attr % (index1 * lines_per_sheet + row /
                                        lines_per_line)))
                        if index2 in [4, 5]:
                            sheet[row + head_end_line, index2].set_value(attr)
                        if index2 >= 9:
                            sheet[row + head_end_line + 1,
                                  index2 + 2 -
                                  attribute_num_per_line].\
                                  set_value((attr % (index1 * lines_per_sheet +
                                                     row / lines_per_line)))
        doc.saveas(template_new_path)
        return True
