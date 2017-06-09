# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models

PRODUCT_STANDARD_UNIT = 'PCS'


class BaseSaleExport(models.Model):
    """Data model of Base Sale Export."""

    _name = "base.sale.export"
    _description = "Base Sale Export"

    @api.multi
    def get_product_hs_code_list(self, so):
        """This function would filter reporting element of hs
        code for each order lines."""
        hs_code_ids = list(set([product.product_hs_code_id.id for product
                                in so.order_line.mapped('product_id')]))
        hs_code_list = self.env['product.hs.code'].browse(hs_code_ids)
        hs_lines = []
        for index, hs_code in enumerate(hs_code_list):
            if not hs_code.ids:
                continue
            hs_lines.append({
                            'index': index,
                            'cn_name': hs_code.cn_name,
                            'hs_code': hs_code.hs_code,
                            'note': hs_code.note,
                            })
        return hs_lines

    @api.multi
    def get_product_sale_list_with_pricelist(self, so):
        """This function would filter order lines of sale order group by the
        same hs code of products inside those line. Quantity and price total
        of lines per hs code would be summed.
        Unit price = summary of price total / summary of quantity"""
        product_pricelist_name = so.pricelist_id.currency_id.name
        hs_code_list = list(set([product.product_hs_code_id for product in
                                 so.order_line.mapped('product_id')]))
        production_lines = []
        for index, hs_code in enumerate(hs_code_list):
            if not hs_code:
                continue
            order_lines_with_same_hs_code =\
                filter(lambda line: line.product_id.product_hs_code_id.id ==
                       hs_code.id, so.order_line)
            qty_with_same_hs_code =\
                sum([line.product_uom_qty for line in
                     order_lines_with_same_hs_code])
            total_price_with_same_hs_code =\
                sum([line.price_total for line in
                     order_lines_with_same_hs_code])
            if qty_with_same_hs_code != 0:
                unit_price_with_same_hs_code =\
                    total_price_with_same_hs_code / qty_with_same_hs_code
                production_lines.append({
                    'unit_price': unit_price_with_same_hs_code
                })
            production_lines.append({
                'hs_code': hs_code,
                'qty': str(qty_with_same_hs_code) + PRODUCT_STANDARD_UNIT,
                'total': total_price_with_same_hs_code,
                'pricelist': product_pricelist_name,
                'index': index
            })
        return production_lines

    @api.multi
    def get_product_sale_list(self, so):
        """This function would filter order lines of sale order group by the
        same hs code of products inside those line. Quantity and price total
        of lines per hs code would be summed.
        Unit price = summary of price
        total / summary of quantity"""
        product_pricelist_sample = so.pricelist_id.currency_id.symbol
        product_pricelist_name = so.pricelist_id.currency_id.name
        hs_code_list = list(set(
            [product.product_hs_code_id for product in
             so.order_line.mapped('product_id')]))
        production_lines = []
        sum_qty = 0
        sum_amount = 0
        for hs_code in hs_code_list:
            if not hs_code:
                continue
            order_lines_with_same_hs_code =\
                filter(lambda line: line.product_id.product_hs_code_id.id ==
                       hs_code.id, so.order_line)
            qty_with_same_hs_code = sum([line.product_uom_qty for line in
                                         order_lines_with_same_hs_code])
            total_price_with_same_hs_code =\
                sum([line.price_total for line in
                     order_lines_with_same_hs_code])
            if qty_with_same_hs_code != 0:
                unit_price_with_same_hs_code =\
                    total_price_with_same_hs_code / qty_with_same_hs_code
                production_lines.append({
                    'unit_price': '@' + product_pricelist_name +
                                  str(unit_price_with_same_hs_code),
                })
            production_lines.append({
                'hs_code': hs_code,
                'qty': str(qty_with_same_hs_code) + PRODUCT_STANDARD_UNIT,
                'total': product_pricelist_name + product_pricelist_sample +
                str(total_price_with_same_hs_code)
            })
            sum_qty += qty_with_same_hs_code
            sum_amount += total_price_with_same_hs_code
        return sum_qty, sum_amount, production_lines

    @api.multi
    def get_product_stock_list(self, sp):
        """This function would filter operation lines of stock picking group by
         the same hs code of products inside those line.
         Carton quantity, total gross weight and total net
         weight of lots of those lines per hs code would be summed."""
        hs_code_ids = list(set([product.product_hs_code_id.id for product in
                                sp.pack_operation_product_ids.mapped(
                                    'product_id')]))
        hs_code_list = self.env['product.hs.code'].browse(hs_code_ids)
        production_lines = []
        sum_carton_quantity = 0
        sum_gross_weight = 0
        sum_net_weight = 0
        sum_volume = 0
        for hs_code in hs_code_list:
            if not hs_code.ids:
                continue
            operation_lines_with_same_hs_code =\
                filter(lambda line: line.product_id.product_hs_code_id.id ==
                       hs_code.id, sp.pack_operation_product_ids)
            operation_lot_ids = [lot_ids.pack_lot_ids for lot_ids in
                                 operation_lines_with_same_hs_code]
            prod_lot_ids = [operation_id.lot_id for operation_id in
                            operation_lot_ids]
            for pack_lot in prod_lot_ids:
                carton_quantity_with_same_hs_code = sum([pack_lot.carton_qty])
                total_gross_weight_with_same_hs_code =\
                    sum([pack_lot.gross_weight])
                total_net_weight_with_same_hs_code = sum([pack_lot.net_weight])
                total_volume_with_same_hs_code = sum([pack_lot.volume])
                production_lines.append({
                    'hs_code': hs_code,
                    'qty_ctn': carton_quantity_with_same_hs_code,
                    'total_gw': total_gross_weight_with_same_hs_code,
                    'total_nw': total_net_weight_with_same_hs_code,
                    'total_meas': total_volume_with_same_hs_code
                })
                sum_carton_quantity += carton_quantity_with_same_hs_code
                sum_gross_weight += total_gross_weight_with_same_hs_code
                sum_net_weight += total_net_weight_with_same_hs_code
                sum_volume += total_volume_with_same_hs_code
        return sum_carton_quantity, sum_gross_weight, sum_net_weight, \
            sum_volume, production_lines

    @api.multi
    def get_package_sum(self, sp):
        """This function would return the sum of quantity, gross weight,
        and volume of packages which was used in this stock picking."""
        if sp.pack_operation_product_ids.mapped('result_package_id'):
            quantity_packages = 0
            total_package_gross_weight = 0
            total_package_meas = 0
            package_list = sp.pack_operation_product_ids.mapped(
                'result_package_id')
            no_repeat_package_ids = list(set(package_list.ids))
            quantity_packages = len(no_repeat_package_ids)
            no_repeat_package_list = self.env['stock.quant.package'].\
                browse(no_repeat_package_ids)
            total_package_gross_weight = sum([package.weight for package in
                                              no_repeat_package_list])
            total_package_meas = sum([package.volume for package in
                                      no_repeat_package_list])
            return quantity_packages, total_package_gross_weight, \
                total_package_meas
        return False
