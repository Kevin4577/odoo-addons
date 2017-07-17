# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
import os


class TestReportPy3oMultisheet(common.TransactionCase):

    def setUp(self):
        super(TestReportPy3oMultisheet, self).setUp()
        self.report_py3o_multisheet_model = self.env['report.py3o.multisheet']

    def test_create_new_template(self):
        Test_sheet_lines_data = {
            'Sheet1': {
                'name': 'Sheet1',
                'lines': 16,
                'duplicate': True,
                'head_end_line': 14,
                'sequence': 1,
                'lines_number': 2
            },
            'Sheet2': {
                'name': 'Sheet2',
                'lines': 16,
                'duplicate': True,
                'head_end_line': 14,
                'sequence': 2,
                'lines_number': 4
            },
            'Sheet3': {
                'name': 'Sheet3',
                'lines': 4,
                'duplicate': True,
                'head_end_line': 14,
                'sequence': 3,
                'lines_number': 8
            }
        }
        attribute_num_per_line = 9
        attribute_per_line = [
            '${data.line%d.index}',
            '${data.line%d.hs_code.hs_code}',
            '${data.line%d.hs_code.name}',
            '${data.line%d.qty}',
            '${objects.ship_info_id%d.ship_to.country_id.name}',
            '${objects.ship_info_id%d.ship_from.country_id.name}',
            '${data.line%d.unit_price}',
            '${data.line%d.total}',
            '${data.line%d.pricelist}',
            '${data.line%d.hs_code.cn_name}',
            '${data.line%d.hs_code.uom_id.name}', ]
        new_path = "tests/customs_declaration_report_template_new.ods"
        base_path = "tests/customs_declaration_report_template.ods"
        template_new_path =\
            os.path.dirname(os.path.dirname(__file__)) + '/' + new_path
        template_base_path =\
            os.path.dirname(os.path.dirname(__file__)) + '/' + base_path
        doc = self.report_py3o_multisheet_model.open_base_template(
            template_base_path)
        sheets = doc.sheets
        self.report_py3o_multisheet_model.multi_sheet_per_template(
            sheets, Test_sheet_lines_data)
        self.report_py3o_multisheet_model.multi_lines_per_sheet(
            sheets, Test_sheet_lines_data)
        self.report_py3o_multisheet_model.multi_attribute_per_line(
            sheets,
            Test_sheet_lines_data,
            attribute_per_line,
            attribute_num_per_line)
        self.report_py3o_multisheet_model.save_new_template(
            template_new_path,
            doc
        )
        print "Test_sheet_lines_data",Test_sheet_lines_data
        head_end_line = Test_sheet_lines_data[sheets[0].name].get(
            'head_end_line', 1)
        import math
        lines_per_line = int(math.ceil(
            len(attribute_per_line) / float(attribute_num_per_line)))
        total_lines_per_sheet = Test_sheet_lines_data[sheets[0].name]['lines']
        summary_line = 'Summary line'
        self.report_py3o_multisheet_model.template_sheet_with_custom_line(
            head_end_line,
            Test_sheet_lines_data,
            attribute_per_line,
            summary_line,
            template_new_path,
            template_base_path
        )



