# -*- coding: utf-8 -*-
#   2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.stock_valuation_report.report.report_stock_valuation_xls \
    import ReportStockValuationProduction, ReportStockValuationParser


class ReportStockValuationProductionInherit(ReportStockValuationProduction):

    def _update_table_info_addition_value(self, val, line):
        """
            This function should be extended to add more value of each row
            inside table of report.
        :param val:
        :param line:
        :return:
        """
        val = super(ReportStockValuationProductionInherit, self). \
            _update_table_info_addition_value(val, line)
        val.update(
            {
                "0": line.product_hs_code_name,
                "1": line.default_code,
                "2": line.product_name,
                "3": line.product_stage_name,
                "4": line.product_line_name,
                "5": line.product_class_name,
                "6": line.product_family_name,
                "7": line.uom_name,
                "8": line.inventory_quantity_before_start_date,
                "9": line.incoming_inventory_quantity,
                "10": line.outgoing_inventory_quantity,
                "11": line.inventory_quantity_before_end_date,
                "12": line.safety_stock_quantity,
                "13": line.below_safety_stock,
                "14": line.location_name
            }
        )
        return val


ReportStockValuationProductionInherit(
    'report.stock.valuation.report.xlsx.product.class.hs.code',
    'wizard.stock.valuation.list',
    parser=ReportStockValuationParser)
