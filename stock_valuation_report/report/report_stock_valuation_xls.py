# -*- coding: utf-8 -*-
#   2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.report import report_sxw
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class ReportStockValuationParser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        """
            Initialize the template of stock valuation report
        :param cr:
        :param uid:
        :param name:
        :param context:
        """

        super(ReportStockValuationParser, self).__init__(
            cr, uid, name, context=context)
        self.context = context
        wanted_list = []
        template_changes = {}
        self.localcontext.update({
            'wanted_list': wanted_list,
            'template_changes': template_changes
        })


class ReportStockValuationProduction(ReportXlsx):
    def __init__(
        self, name, table, rml=False, parser=False, header=True, store=False
    ):
        super(ReportStockValuationProduction, self).__init__(
            name, table, rml, parser, header, store)

    def _write_table_row(self, ws, row, col, data):
        """
            Import each data records into each row of table
        :param ws:
        :param row:
        :param col:
        :param data:
        :return:
        """

        length = len(data)
        for col in range(col, length):
            ws.write(row, col, data[str(col)])

    def _write_table_head(self, ws, row, col, main_title, titles):
        """
            Import the data title into the title of table
        :param ws:
        :param row:
        :param col:
        :param main_title:
        :param titles:
        :return:
        """

        length = len(titles)
        ws.merge_range(0, 0, 0, length - 1, main_title)
        self._write_table_row(ws, row, col, titles)

    def _write_table_info(self, ws, row, col, lines):
        """
            Import each data line into the row of table, more like the
            font size, border size and so on.
        :param ws:
        :param row:
        :param col:
        :param lines:
        :return:
        """

        for line in lines:
            self._write_table_row(ws, row, col, line)
            row += 1

    def _get_xlsx_format(self):
        """
            Get the xlsx format, about font size, color, border size, and so
            on.
        :return:
        """

        borders = {
            'top': 1,
            'left': 1,
            'bottom': 1,
            'right': 1,
            'bottom_color': 0x3A,
        }

        font0 = {
            'font_name': 'Arial',
            'bold': True,
            'font_size': 20,
            'underline': True
        }

        alignment = {
            'align': 'center',
            'valign': 'vcenter'
        }

        style = dict(borders, **font0)
        return dict(alignment, **style)

    def _update_table_info_addition_value(self, val, line):
        """
            This function should be extended to add more value of each row 
            inside table of report.
        :param val: 
        :param line: 
        :return: 
        """
        return {}

    def _get_table_info(self, objects):
        """
            Get each row from table, included information of stock valuation of
            each products.
        :param objects:
        :return:
        """

        result = []

        for line in objects.stock_valuation_lines:
            # save the in the format: col:value
            val = {
                "0": line.default_code,
                "1": line.product_name,
                "2": line.uom_name,
                "3": line.inventory_balance_before_start_date,
                "4": line.incoming_inventory_balance,
                "5": line.outgoing_inventory_balance,
                "6": line.inventory_balance_before_end_date,
                "7": line.safety_stock_level,
                "8": line.below_safety_stock,
                "9": line.location_name
            }
            val.update(self._update_table_info_addition_value(val, line))
            result.append(val)

        return result

    def _get_main_title(self, data):
        """
            Get title of table from table to produce the pdf document.
        :param data:
        :return:
        """

        start_date = data['start_date']
        end_date = data['end_date']
        location = data['location']
        company = data['company']

        return "%s %s to %s Location: %s \"Stock input/\
            output valuation Report\"" % (
            company, start_date, end_date, location)

    def generate_xlsx_report(self, wb, data, objects):
        """
            Build the xlsx report from data of table, and the format which
            already be sot up.
        :param wb:
        :param data:
        :param objects:
        :return:
        """

        # table writer
        ws = wb.add_worksheet('Stock Valuation')
        # style
        style = self._get_xlsx_format()
        wb.add_format(style)
        # col index
        col = 0

        main_title = self._get_main_title(data)

        self._write_table_head(
            ws,
            # start row
            1,
            # start col
            col,
            main_title,
            # title
            data['title'],
        )

        if objects:
            self._write_table_info(
                ws,
                # start row
                2,
                # start col
                col,
                # table info
                self._get_table_info(objects),
            )


ReportStockValuationProduction(
    'report.stock.valuation.report.xlsx', 'wizard.stock.valuation.list',
    parser=ReportStockValuationParser)
