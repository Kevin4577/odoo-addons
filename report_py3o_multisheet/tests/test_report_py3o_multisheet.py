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
        head_end_line = 20
        lines_per_sheet = 8
        total_line_num = 1
        attribute_num_per_line = 9
        attribute_per_line = \
            ['${data.line%d.index}', '${data.line%d.hs_code.hs_code}',
             '${data.line%d.hs_code.name}', '${data.line%d.qty}',
             '${objects.ship_info_id.ship_to.country_id.name}',
             '${objects.ship_info_id.ship_from.country_id.name}',
             '${data.line%d.unit_price}', '${data.line%d.total}',
             '${data.line%d.pricelist}', '${data.line%d.hs_code.cn_name}',
             '${data.line%d.hs_code.uom_id.name}']
        new_path = "/tests/customs_declaration_report_template_new.ods"
        base_path = "/tests/customs_declaration_report_template.ods"
        template_new_path =\
            os.path.dirname(os.path.dirname(__file__)) + '/' + new_path
        template_base_path =\
            os.path.dirname(os.path.dirname(__file__)) + '/' + base_path
        self.report_py3o_multisheet_model.\
            create_new_template(head_end_line, lines_per_sheet,
                                total_line_num, attribute_num_per_line,
                                attribute_per_line, template_new_path,
                                template_base_path)
