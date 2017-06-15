# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

import math
import copy
import logging

_logger = logging.getLogger(__name__)

try:
    from ezodf import opendoc
except (ImportError, IOError) as err:
    _logger.debug(err)


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
        and make the body could be customized by user.
        The whole template should be rendered with the selected delivery
        order data. 'Attribute per line' should be the list of several fields
        of each stock move lines of this delivery order. 4,5 should be the
        index of attribute_per_line to store fields, which would get data from
        delivery order, not from the specific move line. 9 should be the index
        of attribute_per_line, which should start with the second line of
        template.
        attribute_per_line : store fields in list
        total_line_num: product list(lines),
        template_base_path: ODS template file path,
        template_new_path: generate the related path of template_base_path
        """
        lines_per_line = int(math.ceil(len(attribute_per_line
                                           ) / float(attribute_num_per_line)))
        add_sheet_num = int(math.floor(total_line_num / lines_per_sheet))
        doc = opendoc(template_base_path)
        sheets = doc.sheets
        sheet = sheets[0]
        for index in range(add_sheet_num):
            sheet_new = copy.deepcopy(sheet)
            sheets.append(sheet_new)
        for sheet_index, sheet in enumerate(sheets):
            # Append the new sheet
            sheet.insert_rows(index=head_end_line,
                              count=lines_per_sheet * lines_per_line)
            for row in range(0, lines_per_sheet * lines_per_line,
                             lines_per_line):
                for attr_index, attr in enumerate(attribute_per_line):
                    if (sheet_index * lines_per_sheet + row /
                            lines_per_line < total_line_num):
                        # Duplicate the header
                        if attr_index < 4 or 5 < attr_index < 9:
                            sheet[row + head_end_line, attr_index].set_value((
                                attr % (sheet_index * lines_per_sheet + row /
                                        lines_per_line)))
                        # Copy the attribute name
                        if attr_index in [4, 5]:
                            sheet[row + head_end_line, attr_index].\
                                set_value(attr)
                        # Copy the attribute's value
                        if attr_index >= 9:
                            sheet[row + head_end_line + 1,
                                  attr_index + 2 - attribute_num_per_line
                                  ].set_value((attr %
                                               (sheet_index * lines_per_sheet +
                                                row / lines_per_line)))
        doc.saveas(template_new_path)
