# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

import math
import copy
import logging

_logger = logging.getLogger(__name__)

try:
    import ezodf
except (ImportError, IOError) as err:
    _logger.debug(err)


class IrActionsReportXml(models.Model):
    _inherit = 'ir.actions.report.xml'

    py3o_template_fallback_base = fields.\
        Char(size=128, help='If the user does not provide a template'
             ' this one will be used.')


class ReportPy3oMultisheet(models.Model):
    _name = 'report.py3o.multisheet'
    _description = 'Report Py3o Multisheet'

    def open_base_template(self, template_base_path):
        """This function would open the base template ods file
        """
        return ezodf.opendoc(template_base_path)

    def save_new_template(self, template_new_path, doc):
        """This function would generate the new template ods file
        """
        doc.saveas(template_new_path)
        return True

    def multi_sheet_per_template(
            self,
            sheets,
            sheet_lines_data,
    ):
        """This function would generate the new template from base one. It
        would duplicate the head and footer of first sheet or duplicate with
        the empty sheet with specific sheet name.
        sheets: sheets of template ods
        sheet_lines_data:
        {
        'Sheet name':{
                    'name': 'Sheet name',
                    'lines': 'Lines number per sheet',
                    'duplicate': True if need to duplicate head and
                                 foot of base sheet,
                    'head_end_line': The number of the line header
                                     ending
        }
        """
        sheet = sheets[0]
        sheet_list = [value for key, value in sheet_lines_data.items()]
        sheet_list.sort(key=lambda x: x['sequence'])
        for value in sheet_list:
            sheet_new = copy.deepcopy(
                sheet) if value['duplicate'] \
                else ezodf.Table[value['name']]
            sheet_new.name = value['name']
            sheets.append(sheet_new)
        del sheets[0]
        return sheets

    def multi_lines_per_sheet(self, sheets, sheet_lines_data):
        """This function would insert lines into each sheets
        sheet_lines_data:
        {
        'Sheet name':{
                    'name': 'Sheet name',
                    'lines': 'Lines number per sheet',
                    'duplicate': True if need to duplicate head and
                                 foot of base sheet,
                    'head_end_line': The number of the line header
                                     ending
                    },
        }
        """
        for sheet in sheets:
            # Append the new sheet
            lines_per_sheet = \
                sheet_lines_data[sheet.name].get('lines', 1)
            head_end_line = \
                sheet_lines_data[sheet.name].get('head_end_line', 1)
            sheet.insert_rows(index=head_end_line,
                              count=lines_per_sheet)
        return sheets

    def multi_attribute_per_line(
            self,
            sheets,
            sheet_lines_data,
            attribute_per_line,
            attribute_num_per_line,
    ):
        """This function would insert multi-attribute into lines per sheets.
        attribute_per_line: attribute list each lines
        attribute_num_per_line: the number of attributes each lines
        sheet_lines_data:
        {
        'Sheet name':{
                    'name': 'Sheet name',
                    'lines': 'Lines number per sheet',
                    'duplicate': True if need to duplicate head and
                                 foot of base sheet,
                    'head_end_line': The number of the line header
                                     ending
                    },
        }
        """
        lines_per_line = int(math.ceil(
            len(attribute_per_line) / float(attribute_num_per_line)))
        total_lines_num = 0
        for index_sheet, sheet in enumerate(sheets):
            total_lines_per_sheet = sheet_lines_data[sheet.name]['lines']
            lines_per_sheet = total_lines_per_sheet / lines_per_line
            head_end_line = sheet_lines_data[sheet.name]['head_end_line']
            for row in range(0, total_lines_per_sheet, lines_per_line):
                for index_attribute, attr in enumerate(attribute_per_line):
                    index_row = \
                        total_lines_num + row / lines_per_line
                    sheet[row +
                          head_end_line +
                          index_attribute /
                          attribute_num_per_line, index_attribute %
                          attribute_num_per_line].set_value((attr %
                                                             (index_row)))
            total_lines_num += lines_per_sheet
        return sheets
