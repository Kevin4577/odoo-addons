# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _


class WizardStockValuationList(models.TransientModel):
    _name = 'wizard.stock.valuation.list'

    def _get_location(self):
        """
            Get location id from context
        :return:
        """

        location = self.env['stock.location'].search(
            [('id', '=', self._context.get('location_id', False))]
        )

        return location

    def _get_product_inventory_from_product_id(self, stock_historys):
        """
            Filter the stock history with selected product id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('product_id', False):
            stock_historys_new = stock_historys.filtered(
                lambda r: r.product_id.id == self._context.get(
                    'product_id')
            )
            return stock_historys_new
        else:
            return stock_historys

    def _get_product_inventory_from_product_catergory(self, stock_historys):
        """
            Filter the stock history with selected product id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('category_id', False):
            stock_historys_new = stock_historys.filtered(
                lambda r: r.product_categ_id.id ==
                self._context.get('category_id'))
            return stock_historys_new
        else:
            return stock_historys

    def _get_product_inventory_from_lot(self, stock_historys):
        """
            Filter the stock history with selected product id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('lot_id', False):
            stock_history_ids = []
            for stock_history in stock_historys:
                if stock_history.move_id.lot_ids:
                    if self._context.get(
                            'lot_id') in stock_history.move_id.lot_ids.ids:
                        stock_history_ids.append(stock_history.id)
            stock_historys_new = stock_historys.browse(stock_history_ids)
            return stock_historys_new
        else:
            return stock_historys

    def _get_product_inventory_from_package(self, stock_historys):
        """
            Filter the stock history with selected product id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('package_id', False):
            stock_history_ids = []
            for stock_history in stock_historys:
                if stock_history.move_id.linked_move_operation_ids:
                    package_list = \
                        stock_history.move_id.linked_move_operation_ids.mapped(
                            'operation_id'
                        ).mapped('result_package_id')
                    if package_list and self._context.get(
                            'package_id') in package_list.ids:
                        stock_history_ids.append(stock_history.id)
            stock_historys_new = stock_historys.browse(stock_history_ids)
            return stock_historys_new
        else:
            return stock_historys

    def _get_product_inventory_from_partner_customer_id(self, stock_historys):
        """
            Filter the stock history with the selected customer id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('partner_customer_id', False):
            stock_history_ids = []
            for stock_history in stock_historys:
                if stock_history.move_id.picking_id:
                    if stock_history.move_id.picking_id. \
                            picking_type_id.code == 'outgoing':
                        if stock_history.move_id.picking_id.partner_id.id == \
                                self._context.get('partner_customer_id'):
                            stock_history_ids.append(stock_history.id)
            stock_historys_new = stock_historys.browse(stock_history_ids)
            return stock_historys_new
        else:
            return stock_historys

    def _get_product_inventory_from_partner_vendor_id(self, stock_historys):
        """
            Filter the stock history with the selected vendor id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('partner_vendor_id', False):
            stock_history_ids = []
            for stock_history in stock_historys:
                if stock_history.move_id.picking_id:
                    if stock_history.move_id.picking_id. \
                            picking_type_id.code == 'incoming':
                        if stock_history.move_id.picking_id.partner_id.id == \
                                self._context.get('partner_vendor_id'):
                            stock_history_ids.append(stock_history.id)
            stock_historys_new = stock_historys.browse(stock_history_ids)
            return stock_historys_new
        else:
            return stock_historys

    def _get_product_inventory_from_mrp(self, stock_historys):
        """
            Filter the stock history with the selected vendor id from context
        :param stock_historys:
        :return:
        """

        if self._context.get('involved_mrp_order', False):
            stock_history_ids = []
            for stock_history in stock_historys:
                manufacture_order = \
                    stock_history.move_id.raw_material_production_id or \
                    stock_history.move_id.production_id
                if manufacture_order and manufacture_order.id == \
                        self._context.get('involved_mrp_order'):
                    stock_history_ids.append(stock_history.id)
            stock_historys_new = stock_historys.browse(stock_history_ids)
            return stock_historys_new
        else:
            return stock_historys

    def _get_sale_name_from_source(self, origin_and_sales_name, source):
        return origin_and_sales_name.get(source) or ""

    def _get_product_inventory_additonal_filter(self, stock_historys):
        """
            This function could be inherited to filter stock history
            list by additional options.
        """
        return stock_historys

    def _get_product_inventory(self, stock_historys, origin_and_sales_name):
        """
            Get stock history record list, include the filter of shipno,
            product, vendor, customer, location.
        :param stock_historys:
        :param origin_and_sales_name:
        :return:
        """

        products = {}

        if self._context.get('product_id', False):
            stock_historys = \
                self._get_product_inventory_from_product_id(stock_historys)
        elif self._context.get('category_id', False):
            stock_historys = \
                self._get_product_inventory_from_product_catergory(
                stock_historys)
        elif self._context.get('lot_id', False):
            stock_historys = \
                self._get_product_inventory_from_lot(stock_historys)
        elif self._context.get('package_id', False):
            stock_historys = \
                self._get_product_inventory_from_package(stock_historys)
        if self._context.get('partner_customer_id', False):
            stock_historys = \
                self._get_product_inventory_from_partner_customer_id(
                    stock_historys
                )
        elif self._context.get('partner_vendor_id', False):
            stock_historys = \
                self._get_product_inventory_from_partner_vendor_id(
                    stock_historys
                )
        elif self._context.get('involved_mrp_order', False):
            stock_historys = \
                self._get_product_inventory_from_mrp(
                    stock_historys
                )

        stock_historys = \
            self._get_product_inventory_additonal_filter(stock_historys)

        for stock_history in stock_historys:
            sale_name = self._get_sale_name_from_source(
                origin_and_sales_name, stock_history.source)
            key = str(stock_history.product_id.id) + ":" + sale_name

            quantity = stock_history.quantity
            value = stock_history.inventory_value

            if key in products.keys():
                products[key] = {
                    "quantity": products[key]["quantity"] + quantity,
                    "inventory_value":
                        products[key]["inventory_value"] + value,
                    "product": stock_history.product_id,
                    "location": stock_history.location_id,
                    "price_unit_on_quant": stock_history.price_unit_on_quant,
                    "company": stock_history.company_id,
                }
            else:
                products[key] = {
                    "quantity": quantity,
                    "inventory_value": value,
                    "product": stock_history.product_id,
                    "location": stock_history.location_id,
                    "price_unit_on_quant": stock_history.price_unit_on_quant,
                    "company": stock_history.company_id,
                }

        return products

    def _get_product_inventory_before_start_date(self, origin_and_sales_name):
        """
            Filter stock history with the selected start date from context
        :param origin_and_sales_name:
        :return:
        """

        start_date = self._context['start_date']
        location_id = self._context['location_id']
        company_id = self._context['company_id']
        include_child_location = self._context['include_child_location']
        domain = [
            ('date', '<', start_date),
            ('quantity', '!=', 0),
            ('company_id', '=', company_id)
        ]
        if include_child_location:
            domain.append(
                ('location_id', 'child_of', location_id)
            )
        else:
            domain.append(
                ('location_id', '=', location_id)
            )
        stock_historys = self.env['stock.history'].search(domain)
        return self._get_product_inventory(
            stock_historys, origin_and_sales_name)

    def _get_product_inventory_at_end_date(self, origin_and_sales_name):
        """
            Filter stock history with the selected end date from context
        :param origin_and_sales_name:
        :return:
        """

        end_date = self._context['end_date']
        location_id = self._context['location_id']
        company_id = self._context['company_id']
        include_child_location = self._context['include_child_location']
        domain = [
            ('date', '<=', end_date),
            ('quantity', '!=', 0),
            ('company_id', '=', company_id)
        ]
        if include_child_location:
            domain.append(
                ('location_id', 'child_of', location_id)
            )
        else:
            domain.append(
                ('location_id', '=', location_id)
            )
        stock_historys = self.env['stock.history'].search(domain)
        return self._get_product_inventory(
            stock_historys, origin_and_sales_name)

    def _get_product_inventory_between_date(self, origin_and_sales_name):
        """
            Filter stock history between the start date and end date
        :param origin_and_sales_name:
        :return:
        """

        start_date = self._context['start_date']
        end_date = self._context['end_date']
        location_id = self._context['location_id']
        company_id = self._context['company_id']
        include_child_location = self._context['include_child_location']
        domain = [
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('quantity', '!=', 0),
            ('company_id', '=', company_id)
        ]
        if include_child_location:
            domain.append(
                ('location_id', 'child_of', location_id)
            )
        else:
            domain.append(
                ('location_id', '=', location_id)
            )
        stock_historys = self.env['stock.history'].search(domain)
        products = {}
        if self._context.get('product_id', False):
            stock_historys = \
                self._get_product_inventory_from_product_id(stock_historys)
        elif self._context.get('category_id', False):
            stock_historys = \
                self._get_product_inventory_from_product_catergory(
                stock_historys)
        elif self._context.get('lot_id', False):
            stock_historys = \
                self._get_product_inventory_from_lot(stock_historys)
        elif self._context.get('package_id', False):
            stock_historys = \
                self._get_product_inventory_from_package(stock_historys)

        if self._context.get('partner_customer_id', False):
            stock_historys = \
                self._get_product_inventory_from_partner_customer_id(
                    stock_historys
                )
        elif self._context.get('partner_vendor_id', False):
            stock_historys = \
                self._get_product_inventory_from_partner_vendor_id(
                    stock_historys
                )
        elif self._context.get('involved_mrp_order', False):
            stock_historys = \
                self._get_product_inventory_from_mrp(
                    stock_historys
                )

        stock_historys = \
            self._get_product_inventory_additonal_filter(stock_historys)

        for stock_history in stock_historys:
            sale_name = self._get_sale_name_from_source(
                origin_and_sales_name, stock_history.source)

            key = str(stock_history.product_id.id) + ":" + sale_name

            quantity = stock_history.quantity
            value = stock_history.inventory_value

            if key in products.keys():
                if quantity > 0:
                    products[key]["in_quantity"] = \
                        products[key]["in_quantity"] + quantity
                    products[key]["in_inventory_value"] = \
                        products[key]["in_inventory_value"] + value
                    products[key]["location"] = stock_history.location_id
                    products[key][
                        "price_unit_on_quant"] = \
                        stock_history.price_unit_on_quant
                    products[key]["company"] = stock_history.company_id
                else:
                    products[key]["out_quantity"] = \
                        products[key]["out_quantity"] + quantity
                    products[key]["out_inventory_value"] = \
                        products[key]["out_inventory_value"] + value
                    products[key]["location"] = stock_history.location_id
                    products[key][
                        "price_unit_on_quant"] = \
                        stock_history.price_unit_on_quant
                    products[key]["company"] = stock_history.company_id

            else:
                products[key] = {
                    "in_quantity": 0,
                    "in_inventory_value": 0,
                    "out_quantity": 0,
                    "out_inventory_value": 0,
                    "product": stock_history.product_id,
                    "location": stock_history.location_id,
                    "price_unit_on_quant": stock_history.price_unit_on_quant,
                    "company": stock_history.company_id,
                }

                if quantity > 0:
                    products[key]["in_quantity"] = quantity
                    products[key]["in_inventory_value"] = value
                else:
                    products[key]["out_quantity"] = quantity
                    products[key]["out_inventory_value"] = value

        return products

    def _get_source_from_sql(self):
        """
            Get original source list of stock move
        :return:
        """
        user_id = self._context['uid']

        self._cr.execute(
            """select t.origin, s.name
               FROM
               (
                select move.origin, sale_order.name
                FROM stock_move as move
                LEFT JOIN
                    mrp_production ON mrp_production.name = move.origin
                LEFT JOIN
                    purchase_order ON purchase_order.name = move.origin
                LEFT JOIN
                    sale_order ON position(
                        sale_order.name || ':' in mrp_production.origin) > 0 or
                    position(
                        sale_order.name || ':' in purchase_order.origin) > 0
                GROUP BY
                    move.origin,sale_order.name
                ) as t
                LEFT JOIN
                    sale_order as s
                ON
                    t.name = s.name or t.origin = s.name
                JOIN res_users u
                    on u.id = %(int)s
                GROUP BY
                    t.origin, s.name;""",
            {'int': user_id})

        return {rec[0]: rec[1] for rec in self._cr.fetchall()}

    def _get_product_attributes(self, product):
        """
            Get attribute of product to return the dictionary of product with
            each attributes of products
        :param product:
        :return:
        """

        vals = {}

        vals[product.id] = {
            'bottom': "",
            'inside': "",
            'outside': "",
        }
        for attribute_value_id in product.attribute_value_ids:
            if attribute_value_id.attribute_id and attribute_value_id.name:
                if attribute_value_id.attribute_id.name == u'bottom':
                    vals[product.id]['bottom'] = attribute_value_id.name
                if attribute_value_id.attribute_id.name == u'inside':
                    vals[product.id]['inside'] = attribute_value_id.name
                if attribute_value_id.attribute_id.name == u'outside':
                    vals[product.id]['outside'] = attribute_value_id.name
        return vals

    def _compute_safety_stock_level(
            self,
            location,
            product,
            price_unit_on_quant,
            company,
    ):
        """
            This function will compute safety stock level by: min quantity of
            order point of product * unit price of this product. And then
            return it.
        :param location:
        :param product:
        :param price_unit_on_quant:
        :param company:
        :return:
        """
        safe_inventory_amount = self._get_safe_stock_inventory_amount(
            product,
            location.id,
        )
        if safe_inventory_amount:
            if product.cost_method == 'real':
                safety_stock_level = \
                    safe_inventory_amount * price_unit_on_quant
            else:
                safety_stock_level = \
                    safe_inventory_amount * product.get_history_price(
                        company.id,
                        date=self._context.get(
                            'history_date',
                            fields.Datetime.now()
                        )
                    )
            return safety_stock_level
        else:
            return False

    def _get_safe_stock_inventory_amount(self, product, location):
        if product.orderpoint_ids:
            order_point_list = product.orderpoint_ids.filtered(
                lambda r: r.location_id.id == location)
            if order_point_list:
                safe_inventory_amount = min(
                    order_point_list.mapped('product_min_qty'))
                return safe_inventory_amount
            else:
                return False
        else:
            return False

    def _get_stock_valuation_line_additional_value(self, product):
        """
            This function could be extended to add more values to generate
            stock valuation report
        :param product:
        :return:
        """
        return {}

    def _before_date_lines(self, res, lines, lines_before):
        """
            Return the stock valuation list which create date was before
            selected start date
        :param res:
        :param lines:
        :param lines_before:
        :return:
        """

        for key, product in lines_before.items():
            if key not in lines.keys() and product["quantity"] != 0:
                product_id = product['product']
                safety_stock_level = self._compute_safety_stock_level(
                    product['location'],
                    product_id,
                    product['price_unit_on_quant'],
                    product['company'], )
                val = {
                    "default_code": product_id.default_code or "",
                    "product_name": product_id.name,
                    "uom_name": product_id.uom_id.name,
                    "inventory_quantity_before_start_date":
                        product["quantity"],
                    "inventory_balance_before_start_date":
                        product["inventory_value"],
                    "incoming_inventory_quantity": 0,
                    "incoming_inventory_balance": 0,
                    "outgoing_inventory_quantity": 0,
                    "outgoing_inventory_balance": 0,
                    "inventory_quantity_before_end_date": product["quantity"],
                    "inventory_balance_before_end_date":
                        product["inventory_value"],
                    "safety_stock_level": safety_stock_level,
                    "below_safety_stock": 'N' if safety_stock_level > product[
                        "inventory_value"] else 'Y',
                    'location_name': product["location"].name
                }
                val.update(
                    self._get_stock_valuation_line_additional_value(product))
                res.append(val)
        return res

    def _during_date_lines(self, res, lines, lines_before, lines_end):
        """
            Return the stock valuation list which create date was during
            selected date
        :param res:
        :param lines:
        :param lines_before:
        :param lines_end:
        :return:
        """

        for key, product in lines.items():
            product_id = product['product']
            safety_stock_level = self._compute_safety_stock_level(
                product['location'],
                product_id,
                product['price_unit_on_quant'],
                product['company'], )
            val = {
                "default_code": product_id.default_code or "",
                "product_name": product_id.name,
                "uom_name": product_id.uom_id.name,
                "inventory_quantity_before_end_date":
                    lines_end[key]["quantity"],
                "inventory_balance_before_end_date":
                    lines_end[key]["inventory_value"],
                "safety_stock_level": safety_stock_level,
                "location_name": product['location'].name
            }

            val.update(
                self._get_stock_valuation_line_additional_value(product)
            )
            val["incoming_inventory_quantity"] = product["in_quantity"]
            val["incoming_inventory_balance"] = product["in_inventory_value"]
            val["outgoing_inventory_quantity"] = -product["out_quantity"]
            val["outgoing_inventory_balance"] = - product[
                "out_inventory_value"]
            if key in lines_before.keys():
                val['inventory_quantity_before_start_date'] = \
                    lines_before[key]["quantity"]
                val['inventory_balance_before_start_date'] = lines_before[key][
                    "inventory_value"]
            else:
                val['inventory_quantity_before_start_date'] = 0
                val['inventory_balance_before_start_date'] = 0
            val["below_safety_stock"] = 'N' if safety_stock_level > val[
                'inventory_balance_before_end_date'] else 'Y'
            res.append(val)
        return res

    def _load_lines(self):
        """
            Return the stock valuation records to stock valuation view
        :return:
        """

        origin_and_sales_name = self._get_source_from_sql()
        res = []

        lines_before = self._get_product_inventory_before_start_date(
            origin_and_sales_name)
        lines_end = self._get_product_inventory_at_end_date(
            origin_and_sales_name)
        lines = self._get_product_inventory_between_date(origin_and_sales_name)

        self._before_date_lines(res, lines, lines_before)
        self._during_date_lines(res, lines, lines_before, lines_end)
        return sorted(
            res,
            key=lambda rec: (
                rec['default_code'],
                rec['product_name']))

    def _get_table_title(self):
        """
            Save the format in col:title to show on the stock valuation report
            view
        :return:
        """

        title = {
            0: _("Default Code"),
            1: _("Product Name"),
            2: _("Unit of Measure"),
            3: _("Inventory Balance Before Start Date"),
            4: _("Incoming Inventory Balance"),
            5: _("Outgoing Inventory Balance"),
            6: _("Inventory Balance Before End Date"),
            7: _("Safety Stock Level"),
            8: _("Below Safety Stock"),
            9: _("Location Name")
        }
        return title

    def _get_company_name(self):
        """
            Get company name from default user
        :return:
        """

        company_id = self._context.get('company_id', False)

        return company_id

    stock_valuation_lines = fields.One2many(
        'wizard.stock.valuation.line',
        'stock_valuation_list_id',
        string='Stock Valuation lines',
        readonly=True,
        default=_load_lines
    )

    location_id = fields.Many2one(
        'stock.location',
        'Location',
        readonly=True,
        default=_get_location
    )

    @api.one
    def export(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def xlsx_export(self):
        """
            Produce xlsx report based on the data report produced
        :return:
        """

        datas = {
            'model': 'wizard.stock.valuation.list',
            'title': self._get_table_title(),
            'start_date': self._context['start_date'] or "",
            'end_date': self._context['end_date'] or "",
            'location': self._context['location'] or "",
            'company': self._get_company_name()
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'stock.valuation.report.xlsx',
            'datas': datas
        }


class WizardStockValuationLine(models.TransientModel):
    _name = 'wizard.stock.valuation.line'

    stock_valuation_list_id = fields.Many2one(
        'wizard.stock.valuation.list',
        'Stock Valuation list',
        ondelete='cascade',
        index=True,
        help='Stock Valuation list'
    )
    product_name = fields.Char(
        'Product Name',
        readonly=True,
        default="",
        help='Product'
    )
    uom_name = fields.Char(
        'Unit of Measure',
        readonly=True,
        default="",
        help='Unit of Measure'
    )
    default_code = fields.Char(
        'Internal Reference',
        readonly=True,
        default="",
        help='Internal Reference'
    )
    inventory_balance_before_start_date = fields.Float(
        'Inventory Balance Before Start Date',
        readonly=True,
        default=0,
        help='Total inventory balance before start date.'
    )
    incoming_inventory_balance = fields.Float(
        'Incoming Inventory Balance',
        readonly=True,
        default=0,
        help='Incoming inventory balance between start date and end date.'
    )
    outgoing_inventory_balance = fields.Float(
        'Outgoing Inventory Balance',
        readonly=True,
        default=0,
        help='Outgoing inventory balance between start date and end date.'
    )
    inventory_balance_before_end_date = fields.Float(
        'Inventory Balance Before End Date',
        readonly=True,
        default=0,
        help='Inventory balance before end date.'
    )
    safety_stock_level = fields.Float(
        'Safety Stock Level',
        readonly=True,
        default=0,
        help='Safety Stock Level.'
    )
    below_safety_stock = fields.Char(
        'Below Safety Stock?',
        readonly=True,
        default="",
        help='Whether current inventory balance was in the safety stock level.'
    )
    location_name = fields.Char(
        'Location',
        readonly=True,
        default="",
        help='Stock location.'
    )
