# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from datetime import datetime


class TradingInvoice(models.Model):

    _name = "trading.invoice"
    _description = "Trading Invoice"

    @api.multi
    def get_order_lines(self, stock_picking):
        """This function get the product information of each order lines
        inside sale order."""
        order_lines = stock_picking.move_lines.mapped('procurement_id'
                                                      ).mapped('sale_line_id')
        product_lines = []
        for index, line in enumerate(order_lines):
            product_lines.append({
                'index': index,
                'product_id': line.product_id,
                'name': line.name,
                'product_uom': line.product_uom,
                'price_unit': line.price_unit,
                'qty': line.product_uom_qty,
                'price_total': line.price_total,
            })
        sum_qty = 0.0
        sum_amount = 0.0
        for line in product_lines:
            sum_qty += line['qty']
            sum_amount += line['price_total']
        return {
            'sum_qty': sum_qty,
            'sum_amount': sum_amount,
            'product_lines': product_lines,
        }

    @api.multi
    def get_product_lot_list_per_sale_order(self, stock_picking_list):
        """This function get the lot detail of each delivery order lines,
        which was group by client order reference of sale order for each
        of them."""
        product_lines = []
        sale_order_obj = self.env['sale.order']
        sale_order_list = sale_order_obj.\
            browse(list(set(stock_picking_list.mapped('sale_id').ids)))
        for sale_order in sale_order_list:
            client_order_ref = sale_order.client_order_ref
            stock_picking_per_sale_order = \
                stock_picking_list.\
                filtered(lambda stock_picking: stock_picking.sale_id.id ==
                         sale_order.id)
            operation_lines_per_sale_order = stock_picking_per_sale_order.\
                mapped('pack_operation_product_ids')
            for operation_line in operation_lines_per_sale_order:
                for operation_lot_line in operation_line.pack_lot_ids:
                    product_lines.append({
                        'shipping_marks': '',
                        'client_order_ref': client_order_ref,
                        'product_id':
                        operation_line.product_id,
                        'qty': operation_lot_line.qty,
                        'carton_qty':
                        operation_lot_line.lot_id.carton_qty,
                        'track_order': '',
                    })
        sum_product_qty = 0.0
        sum_carton_qty = 0.0
        for line in product_lines:
            sum_product_qty += line['qty']
            sum_carton_qty += line['carton_qty']
        return {
            'sum_product_qty': sum_product_qty,
            'sum_carton_qty': sum_carton_qty,
            'product_lines': product_lines,
            'location_id': stock_picking_list[0].location_id or
            self.env['stock.location'],
            'delivery_date': stock_picking_list[0].min_date or
            self.env['stock.picking'],
            'delivery_name': stock_picking_list[0].name or
            self.env['stock.picking'],
            'team_id': stock_picking_list[0].sale_id.team_id or
            self.env['crm.team'],
        }

    @api.multi
    def get_product_order_list_with_qty(self, stock_picking_list):
        """This function get the order quantity and delivery quantity of order
        lines, which was group by client order reference of sale order for
        each of them."""
        sale_order_obj = self.env['sale.order']
        sale_order_list = sale_order_obj.\
            browse(list(set(stock_picking_list.mapped('sale_id').ids)))
        sale_order_lines = sale_order_list.mapped('order_line')
        lot_list = stock_picking_list.mapped('pack_operation_product_ids'
                                             ).mapped('pack_lot_ids'
                                                      ).mapped('lot_id')
        package_list = stock_picking_list.mapped('pack_operation_product_ids'
                                                 ).mapped('result_package_id')
        pallet_sum = sum([lot.carton_qty for lot in lot_list])
        gw_sum_without_package = sum([lot.gross_weight for lot in lot_list])
        gw_sum_package = sum([package.weight for package in package_list])
        gw_sum = gw_sum_package + gw_sum_without_package
        product_lines = []
        for order_line in sale_order_lines:
            product_lines.append({
                'product_id': order_line.product_id,
                'client_order_ref': order_line.order_id.client_order_ref,
                'product_uom_qty': order_line.product_uom_qty,
                'qty_delivered': order_line.qty_delivered
            })
        sum_qty = 0.0
        sum_qty_delivered = 0.0
        for line in product_lines:
            sum_qty += line['product_uom_qty']
            sum_qty_delivered += line['qty_delivered']
        return {
            'sum_qty': sum_qty,
            'sum_qty_delivered': sum_qty_delivered,
            'product_lines': product_lines,
            'pallet_sum': pallet_sum,
            'gw_sum': gw_sum,
            'partner_id': stock_picking_list[0].partner_id or
            self.env['res.partner'],
            'confirmation_date':
            stock_picking_list[0].sale_id.confirmation_date or
            self.env['sale.order'],
            'min_date': stock_picking_list[0].min_date,
            'ship_info_id': stock_picking_list[0].ship_info_id or
            self.env['shipping'],
            'partner_shipping_id':
            stock_picking_list[0].sale_id.partner_shipping_id or
            self.env['res.partner'],
            'payment_term_id': stock_picking_list[0].sale_id.payment_term_id or
            self.env['account.payment.term'],
            'package_no': package_list[0].forwarder_no or
            self.env['stock.quant.package']
        }

    @api.multi
    def get_product_lot_list_per_package_number(self, stock_picking_list):
        """This function get the lot detail and package number of each
        delivery order lines, which was group by client order reference of
        sale order for each of them."""
        sale_order_obj = self.env['sale.order']
        sale_order_list = sale_order_obj.\
            browse(list(set(stock_picking_list.mapped('sale_id').ids)))
        product_lines = []
        for sale_order in sale_order_list:
            for sale_order in sale_order_list:
                client_order_ref = sale_order.client_order_ref
                stock_picking_per_sale_order = stock_picking_list.\
                    filtered(lambda stock_picking: stock_picking.sale_id.id ==
                             sale_order.id)
                operation_lines_per_sale_order = stock_picking_per_sale_order.\
                    mapped('pack_operation_product_ids')
                for operation_line in operation_lines_per_sale_order:
                    package_number = \
                        operation_line.result_package_id.forwarder_no
                    for operation_lot_line in operation_line.pack_lot_ids:
                        product_lines.append({
                            'package_no': package_number,
                            'client_order_ref': client_order_ref,
                            'customer_product_code':
                            operation_line.product_id.customer_product_code,
                            'qty': operation_lot_line.qty,
                            'carton_qty': operation_lot_line.lot_id.carton_qty,
                            'gw_lot': operation_lot_line.lot_id.gross_weight,
                            'means_lot': operation_lot_line.lot_id.volume,
                        })
        sum_qty = 0.0
        pallet_sum = 0.0
        sum_gw = 0.0
        sum_meas = 0.0
        print_date = datetime.today().strftime('%Y-%m-%d')
        for line in product_lines:
            sum_qty += line['qty']
            pallet_sum += line['carton_qty']
            sum_gw += line['gw_lot']
            sum_meas += line['means_lot']
        return {
            'sum_qty': sum_qty,
            'pallet_sum': pallet_sum,
            'product_lines': product_lines,
            'ship_to': stock_picking_list[0].ship_info_id.ship_to or
            self.env['res.partner'],
            'sum_gw': sum_gw,
            'sum_meas': sum_meas,
            'print_date': print_date,
        }

    @api.multi
    def get_order_lines_per_invoice(self, account_invoice):
        """This function returns the sum of quantity, unit price, and
        amount of order line which was used in this account invoice."""
        sale_order_list = account_invoice.invoice_line_ids.\
            mapped('sale_line_ids').mapped('order_id')
        sale_order_lists = []
        for sale_order in sale_order_list:
            account_invoice_lines_per_same_order = \
                account_invoice.invoice_line_ids.\
                filtered(lambda line: sale_order.id in line.sale_line_ids.
                         mapped('order_id').ids)
            sale_order_lists.append({
                'sale_order_name': sale_order.name,
                'client_order_ref': sale_order.client_order_ref,
                'invoice_items': account_invoice_lines_per_same_order,
            })
            sum_qty = 0.0
            sum_amount = 0.0
            for line in sale_order_lists[0].get('invoice_items'):
                sum_qty += line.quantity
                sum_amount += line.price_subtotal
        ship_information = sale_order_list.picking_ids[0].ship_info_id or\
            self.env['shipping']
        return {
            'sale_order_list': sale_order_lists,
            'sum_qty': sum_qty,
            'sum_amount': sum_amount,
            'ship_from': ship_information.ship_from,
            'ship_to': ship_information.ship_to,
            'ship_by': ship_information.ship_by
        }

    @api.multi
    def get_detail_lot_list_per_invoice(self, account_invoice):
        """This function returns the sum of gross weight, carton quantity,
        and volume of lot list, which was used in delivery order and
        related to this account invoice."""
        sale_order_obj = self.env['sale.order']
        sale_order_lines = \
            account_invoice.invoice_line_ids.mapped('sale_line_ids')
        sale_order_ids = sale_order_lines.mapped('order_id').ids
        sale_order_list = sale_order_obj.browse(list(set(sale_order_ids)))
        pack_operation_list = sale_order_lines.\
            mapped('procurement_ids'
                   ).mapped('move_ids').mapped('linked_move_operation_ids'
                                               ).mapped('operation_id')
        package_ids = \
            list(set(pack_operation_list.mapped('result_package_id').ids))
        stock_quant_package = self.env['stock.quant.package']
        package_list = stock_quant_package.browse(package_ids)
        pallet_total = 0.0
        total_gw = 0.0
        total_nt = 0.0
        total_meas = 0.0
        package_lists = []
        for package in package_list:
            gw_package = package.weight
            meas_package = package.volume
            order_list = []
            pallet_sum = 0.0
            sum_gw = 0.0
            sum_nt = 0.0
            sum_meas = 0.0
            if sale_order_list:
                sub_list = self.\
                    get_detail_lot_list_per_invoice_sub_list(sale_order_list,
                                                             package,
                                                             sale_order_lines)
            sub_list = sub_list or {}
            package_lists.append({
                'order_list': sub_list['order_list'] or order_list or False,
                'pallet_sum': sub_list['pallet_sum'] or pallet_sum,
                'sum_gw': sub_list['sum_gw'] or sum_gw + gw_package,
                'sum_nt': sub_list['sum_nt'] or sum_nt,
                'sum_meas': sub_list['sum_meas'] or sum_meas + meas_package,
                'package_qty': 1,
            })
            pallet_total += sub_list['pallet_sum']
            total_gw += sub_list['sum_gw']
            total_nt += sub_list['sum_nt']
            total_meas += sub_list['sum_meas']
        return {
            'package_list': package_lists,
            'total_gw': total_gw,
            'total_nt': total_nt,
            'total_meas': total_meas,
            'pallet_total': pallet_total,
            'package_total': len(package_list),
            'ship_info_id': sale_order_list.picking_ids[0].ship_info_id or\
                self.env['shipping'],
        }

    @api.multi
    def get_detail_lot_list_per_invoice_sub_list(self, sale_order_list,
                                                 package, sale_order_lines):
        order_list = []
        pallet_sum = 0.0
        sum_gw = 0.0
        sum_nt = 0.0
        sum_meas = 0.0
        for sale_order in sale_order_list:
            pack_operation_list_per_same_sale_order =\
                sale_order_lines.\
                filtered(lambda line: line.order_id.id == sale_order.id).\
                mapped('procurement_ids').mapped('move_ids').\
                mapped('linked_move_operation_ids').\
                mapped('operation_id').\
                filtered(lambda operation:
                         operation.result_package_id.id == package.id)
            pack_operation_lot_list_per_same_sale_order =\
                pack_operation_list_per_same_sale_order.\
                mapped('pack_lot_ids')
            if pack_operation_lot_list_per_same_sale_order:
                order_lines = self.\
                    get_detail_lot_list_per_invoice_sub(
                        pack_operation_lot_list_per_same_sale_order)
            order_lines = order_lines or []
            pallet_sum_per_same_sale_order = 0.0
            sum_gw_per_same_sale_order = 0.0
            sum_nt_per_same_sale_order = 0.0
            sum_meas_per_same_sale_order = 0.0
            for line in order_lines:
                pallet_sum_per_same_sale_order += line['carton_qty']
                sum_gw_per_same_sale_order += line['gross_weight']
                sum_nt_per_same_sale_order += line['net_weight']
                sum_meas_per_same_sale_order += line['volume']
            order_list.append({
                'name': sale_order.name,
                'client_order_ref': sale_order.client_order_ref,
                'lines': order_lines,
            })
            pallet_sum += pallet_sum_per_same_sale_order
            sum_gw += sum_gw_per_same_sale_order
            sum_nt += sum_nt_per_same_sale_order
            sum_meas += sum_meas_per_same_sale_order
        return {
            'order_list': order_list,
            'pallet_sum': pallet_sum,
            'sum_gw': sum_gw,
            'sum_nt': sum_nt,
            'sum_meas': sum_meas
        }

    @api.multi
    def get_detail_lot_list_per_invoice_sub(self,
                                            operation_lot_list_sale_order):
        order_lines = []
        for pack_operation_lot in operation_lot_list_sale_order:
            order_lines.append({
                'carton_no': pack_operation_lot.lot_id.carton_no,
                'customer_product_code':
                pack_operation_lot.operation_id.product_id.
                customer_product_code,
                'qty': pack_operation_lot.qty,
                'gross_by_carton':
                pack_operation_lot.lot_id.gross_by_carton,
                'net_by_carton':
                pack_operation_lot.lot_id.net_by_carton,
                'carton_qty': pack_operation_lot.lot_id.carton_qty,
                'gross_weight': pack_operation_lot.lot_id.gross_weight,
                'net_weight': pack_operation_lot.lot_id.net_weight,
                'volume': pack_operation_lot.lot_id.volume,
                'volume_per_carton': pack_operation_lot.lot_id.volume /
                pack_operation_lot.lot_id.carton_qty,
            })
        return order_lines

    @api.multi
    def get_invoice_lines_per_invoice(self, account_invoice):
        """This function returns the sum of quantity, unit price, and amount
        of invoice lines which was used in this account invoice."""
        product_lines = []
        for index, line in enumerate(account_invoice.invoice_line_ids):
            product_lines.append({
                'index': index,
                'product_id': line.product_id,
                'qty': line.quantity,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal
            })
        return {
            'product_lines': product_lines
        }

    @api.multi
    def get_package_name_per_package_list(self, stock_picking_list):
        """This function prepares for the stock picking list with the related
        package type names and related package name"""
        product_packaging_object = self.env['product.packaging']
        package_type_ids = stock_picking_list.\
            mapped('pack_operation_product_ids'
                   ).mapped('result_package_id').mapped('packaging_id').ids
        package_type_list = product_packaging_object.\
            browse(list(set(package_type_ids)))
        package_list = []
        for package_type in package_type_list:
            pack_operation_lines_per_same_package_type = \
                stock_picking_list.mapped('pack_operation_product_ids').\
                filtered(lambda operation:
                         operation.result_package_id.packaging_id.id ==
                         package_type.id)
            pack_operation_lot_list_per_same_package_type = \
                pack_operation_lines_per_same_package_type.\
                mapped('pack_lot_ids')
            package_list_per_same_package_type = \
                pack_operation_lines_per_same_package_type.\
                mapped('result_package_id')
            package_list.append({
                'name': package_type.name,
                'lines_number':
                len(pack_operation_lot_list_per_same_package_type),
                'list': package_list_per_same_package_type.mapped('name'),
            })
        return package_list

    @api.multi
    def get_pack_lot_list_per_package_type(self, stock_picking_list):
        """This function returns package type names and package name of each
        package type, which is used in stock picking list"""
        package_no = stock_picking_list.mapped('pack_operation_product_ids'
                                               ).mapped('result_package_id'
                                                        )[0].forwarder_no
        partner_shipping_id = stock_picking_list[0].ship_info_id.ship_to or\
            self.env['res.partner']
        package_type_list = stock_picking_list.\
            mapped('pack_operation_product_ids'
                   ).mapped('result_package_id').mapped('packaging_id')
        for package_type in package_type_list:
            pack_operation_lines_per_same_package_type = \
                stock_picking_list.mapped('pack_operation_product_ids').\
                filtered(lambda operation:
                         operation.result_package_id.packaging_id.id ==
                         package_type.id)
            pack_operation_lot_list_per_same_package_type = \
                pack_operation_lines_per_same_package_type.\
                mapped('pack_lot_ids')
            pack_lot_list = []
            for pack_lot in pack_operation_lot_list_per_same_package_type:
                pack_lot_list.append({
                    'client_order_ref':
                    pack_lot.operation_id.picking_id.sale_id.client_order_ref,
                    'product_id': pack_lot.operation_id.product_id,
                    'product_uom': pack_lot.operation_id.product_uom_id.name,
                    'product_uom_qty': pack_lot.qty_todo,
                    'qty_delivery': pack_lot.qty,
                    'carton_qty': pack_lot.lot_id.carton_qty
                })
            package_list = []
            package_list.append({package_type.name: pack_lot_list})
            return {
                'package_no': package_no,
                'partner_shipping_id': partner_shipping_id,
                'package_list': package_list
            }
