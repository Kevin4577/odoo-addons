# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,\
    DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

PRODUCT_STANDARD_UNIT = 'PCS'


class TradingSale(models.Model):
    """Data model of Base Sale Export."""

    _name = "trading.sale"
    _description = "Trading Sale"

    @api.multi
    def get_date_invoice(self, account_invoice):
        date_invoice = datetime. \
            strftime(datetime.strptime(
                account_invoice.create_date,
                DEFAULT_SERVER_DATETIME_FORMAT
            ), DEFAULT_SERVER_DATE_FORMAT) if \
            not account_invoice.date_invoice else account_invoice.date_invoice
        return {
            'date_invoice': date_invoice
        }

    @api.multi
    def get_customer(self, company):
        """
        This function provided the customer information of sale order
        :param sale_order:
        :return:
        """
        company_bank_list = company.partner_id.bank_ids
        company_main_bank = \
            company_bank_list[0] if company_bank_list else False
        return {
            'bank_name':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.name or '',
            'bank_account':
                company_main_bank and company_main_bank.acc_number or '',
            'bank_street':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.street or '',
            'bank_street2':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.street2 or '',
            'bank_city':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.city or '',
            'bank_zip':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.zip or '',
            'bank_state':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.state and
                company_main_bank.bank_id.state.name or '',
            'bank_country':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.country and
                company_main_bank.bank_id.country.name or '',
            'bank_phone':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.phone or '',
            'bank_fax':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.fax or '',
            'bank_bic':
                company_main_bank and company_main_bank.bank_id and
                company_main_bank.bank_id.bic or '',
            'bank_holder':
                company_main_bank and company_main_bank.partner_id and
                company_main_bank.partner_id or self.env['res.partner'],
        }

    @api.multi
    def get_product_hs_code_list(self, so):
        """This function would filter reporting element of hs
        code for each order lines."""
        product_list = so.order_line.mapped('product_id')
        hs_lines = []
        for index, product in enumerate(product_list):
            if product.ids:
                hs_lines.append({
                                'index': index,
                                'cn_name': product.product_hs_code_id.cn_name,
                                'hs_code': product.product_hs_code_id.hs_code,
                                'note': product.hs_code_note,
                                })
        return hs_lines

    @api.multi
    def get_product_sale_list_with_pricelist(self, account_invoice):
        """This function would filter order lines of sale order group by the
        same hs code of products inside those line. Quantity and price total
        of lines per hs code would be summed.
        Unit price = summary of price total / summary of quantity"""
        product_pricelist_name = account_invoice.currency_id.name
        hs_code_list = account_invoice.mapped('invoice_line_ids'). \
            mapped('product_id').mapped('product_hs_code_id')
        production_lines = []
        for index, hs_code in enumerate(hs_code_list):
            production_dict = {}
            if hs_code:
                order_lines_with_same_hs_code =\
                    filter(lambda line:
                           line.product_id.product_hs_code_id.id ==
                           hs_code.id,
                           account_invoice.mapped('invoice_line_ids'))
                qty_with_same_hs_code =\
                    sum([line.quantity for line in
                         order_lines_with_same_hs_code])
                total_price_with_same_hs_code =\
                    sum([line.price_subtotal for line in
                         order_lines_with_same_hs_code])
                if qty_with_same_hs_code != 0:
                    unit_price_with_same_hs_code =\
                        total_price_with_same_hs_code / qty_with_same_hs_code
                    production_dict.update({
                        'unit_price':
                            '{:.4f}'.format(unit_price_with_same_hs_code)
                    })
                production_dict.update({
                    'hs_code': hs_code,
                    'qty': str(int(qty_with_same_hs_code)),
                    'total': '{:.2f}'.format(total_price_with_same_hs_code),
                    'pricelist': product_pricelist_name,
                    'index': index + 1,
                })
                production_lines.append(production_dict)
        return production_lines

    @api.multi
    def get_product_sale_list_for_purchase(self, sp):
        """This function would filter order lines of sale order group by the
        same hs code of products inside those line. Quantity and price total
        of lines per hs code would be summed. This report would be provided
        for the purchase department to make purchase order base on the sale
        order.
        Unit price = summary of price
        total / summary of quantity"""
        product_pricelist_sample = sp.sale_id.pricelist_id.currency_id.symbol
        product_pricelist_name = sp.sale_id.pricelist_id.currency_id.name
        hs_code_list = list(set(
            [product.product_hs_code_id for product in
             sp.pack_operation_product_ids.mapped('product_id')]))
        sale_order_lines = sp.pack_operation_product_ids.\
            mapped('linked_move_operation_ids').mapped('move_id').\
            mapped('procurement_id').mapped('sale_line_id')
        production_lines = []
        sum_qty = 0
        sum_amount = 0
        for hs_code in hs_code_list:
            production_dict = {}
            if hs_code:
                order_lines_with_same_hs_code = \
                    filter(lambda line:
                           line.product_id.product_hs_code_id.id ==
                           hs_code.id,
                           sale_order_lines)
                qty_with_same_hs_code = sum([line.product_uom_qty for line in
                                             order_lines_with_same_hs_code])
                total_price_with_same_hs_code = \
                    sum([line.price_subtotal for line in
                         order_lines_with_same_hs_code])
                unit_price_with_same_hs_code = 0
                if qty_with_same_hs_code != 0:
                    unit_price_with_same_hs_code = \
                        total_price_with_same_hs_code / qty_with_same_hs_code
                production_dict.update({
                    'unit_price': '@' + product_pricelist_name +
                                  str(unit_price_with_same_hs_code)
                })
                production_dict.update({
                    'hs_code': hs_code,
                    'qty': str(qty_with_same_hs_code) + PRODUCT_STANDARD_UNIT,
                    'total':
                        product_pricelist_name + product_pricelist_sample +
                        str(total_price_with_same_hs_code)
                })
                production_lines.append(production_dict)
                sum_qty += qty_with_same_hs_code
                sum_amount += total_price_with_same_hs_code
        return sum_qty, sum_amount, production_lines

    @api.multi
    def get_product_sale_list(self, account_invoice):
        """This function would filter order lines of sale order group by the
        same hs code of products inside those line. Quantity and price total
        of lines per hs code would be summed.
        Unit price = summary of price
        total / summary of quantity"""
        product_pricelist_sample = account_invoice.currency_id.symbol
        product_pricelist_name = account_invoice.currency_id.name
        hs_code_list = list(set(
            [product.product_hs_code_id for product in
             account_invoice.mapped('invoice_line_ids').mapped('product_id')]))
        production_lines = []
        sum_qty = 0
        sum_amount = 0
        for hs_code in hs_code_list:
            production_dict = {}
            if hs_code:
                order_lines_with_same_hs_code =\
                    filter(lambda line:
                           line.product_id.product_hs_code_id.id ==
                           hs_code.id,
                           account_invoice.mapped('invoice_line_ids'))
                qty_with_same_hs_code = sum([line.quantity for line in
                                             order_lines_with_same_hs_code])
                total_price_with_same_hs_code =\
                    sum([line.price_subtotal for line in
                         order_lines_with_same_hs_code])
                if qty_with_same_hs_code != 0:
                    unit_price_with_same_hs_code =\
                        total_price_with_same_hs_code / qty_with_same_hs_code
                    production_dict.update({
                        'unit_price': '@' + product_pricelist_name +
                                      str(unit_price_with_same_hs_code)
                    })
                production_dict.update({
                    'hs_code': hs_code,
                    'qty': str(qty_with_same_hs_code) + PRODUCT_STANDARD_UNIT,
                    'total':
                        product_pricelist_name + product_pricelist_sample +
                    str(total_price_with_same_hs_code)
                })
                production_lines.append(production_dict)
                sum_qty += qty_with_same_hs_code
                sum_amount += total_price_with_same_hs_code
        return sum_qty, sum_amount, production_lines

    @api.multi
    def get_product_stock_list(self, account_invoice):
        """This function would filter operation lines of stock picking group by
         the same hs code of products inside those line.
         Carton quantity, total gross weight and total net
         weight of lots of those lines per hs code would be summed."""
        stock_picking_obj = self.env['stock.picking']
        stock_picking_list = \
            stock_picking_obj.search([('invoice_id', '=', account_invoice.id)])
        pack_operation_list = \
            stock_picking_list.mapped('pack_operation_product_ids')
        hs_code_list = account_invoice.mapped('invoice_line_ids').\
            mapped('product_id').mapped('product_hs_code_id')
        production_lines = []
        sum_carton_quantity = 0
        sum_gross_weight = 0
        sum_net_weight = 0
        sum_volume = 0
        for hs_code in hs_code_list:
            if hs_code.ids:
                operation_lines_with_same_hs_code = \
                    pack_operation_list.filtered(
                        lambda line:
                        line.product_id.product_hs_code_id.id == hs_code.id)
                prod_lot_ids = \
                    operation_lines_with_same_hs_code.\
                    mapped('pack_lot_ids').\
                    mapped('lot_id')

                production_lines.append({
                    'hs_code': hs_code,
                    'qty_ctn': sum(prod_lot_ids.mapped('carton_qty')),
                    'total_gw': sum(prod_lot_ids.mapped('gross_weight')),
                    'total_nw': sum(prod_lot_ids.mapped('net_weight')),
                    'total_meas': sum(prod_lot_ids.mapped('volume'))
                })
                for pack_lot in prod_lot_ids:
                    carton_quantity_with_same_hs_code = sum(
                        [pack_lot.carton_qty])
                    total_gross_weight_with_same_hs_code =\
                        sum([pack_lot.gross_weight])
                    total_net_weight_with_same_hs_code = sum(
                        [pack_lot.net_weight])
                    total_volume_with_same_hs_code = sum([pack_lot.volume])
                    sum_carton_quantity += carton_quantity_with_same_hs_code
                    sum_gross_weight += total_gross_weight_with_same_hs_code
                    sum_net_weight += total_net_weight_with_same_hs_code
                    sum_volume += total_volume_with_same_hs_code
        return int(sum_carton_quantity), sum_gross_weight, sum_net_weight, \
            sum_volume, production_lines

    @api.multi
    def get_package_sum(self, account_invoice):
        """This function would return the sum of quantity, gross weight,
        and volume of packages which was used in this stock picking."""
        stock_picking_obj = self.env['stock.picking']
        stock_picking_list = \
            stock_picking_obj.search([('invoice_id', '=', account_invoice.id)])
        pack_operation_list = \
            stock_picking_list.mapped('pack_operation_product_ids')
        package_list = pack_operation_list.mapped('result_package_id')
        if package_list:
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
        return 0, 0, 0
