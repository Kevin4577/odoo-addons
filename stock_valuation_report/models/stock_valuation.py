# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import calendar
import datetime
from odoo import api, fields, models, _
from lxml import etree
from odoo.exceptions import UserError


class StockValuation(models.Model):
    _name = 'stock.valuation'

    @api.model
    def fields_view_get(
            self, view_id=None, view_type='form',
            toolbar=False, submenu=False):
        """
            Return the available location list of current company to the stock
            valuation wizard report view.
        :param view_id:
        :param view_type:
        :param toolbar:
        :param submenu:
        :return:
        """

        res = super(StockValuation, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        loc_ids = []
        loc_view_ids = []
        if self._uid:
            cur_user = self.env['res.users'].browse(self._uid)
            warehouse_list = self.env['stock.warehouse'].search([
                ('company_id', '=', cur_user.company_id.id)
            ])
            for warehouse in warehouse_list:
                loc_view_ids.append(warehouse.view_location_id.id)
            for loc_view in loc_view_ids:
                loc_list = self.env['stock.location'].search([
                    ('location_id', 'child_of', loc_view)
                ])
                for loc in loc_list:
                    loc_ids.append(loc.id)
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='location_id']"):
                node.set('domain', "[('id', 'in', %s)]" % (loc_ids))
            res['arch'] = etree.tostring(doc)
        return res

    def _get_first_date(self):
        """
            Get start date of current month
        :return:
        """

        now = datetime.datetime.now()
        # set the date to the first day of the month
        return datetime.datetime(now.year, now.month, 1)

    def _get_last_date(self):
        """
            Get end date of current month
        :return:
        """

        now = datetime.datetime.now()
        # return value [first_day, last_day]
        month_range = calendar.monthrange(now.year, now.month)

        # set the date to the end day of the month
        return datetime.datetime(now.year, now.month, month_range[1])

    @api.model
    def _default_location_id(self):
        company_user = self.env.user.company_id
        warehouse = self.env['stock.warehouse'].search(
            [('company_id', '=', company_user.id)], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        else:
            raise UserError(
                _('You must define a warehouse for the company: %s.') % (
                    company_user.name,))

    @api.model
    def _selection_filter_by_product(self):
        """ Get the list of filter allowed according to the options checked
        in 'Settings\Warehouse'. """
        res_filter = [
            ('none', _('All products')),
            ('product', _('One product only')),
            ('category', _('One product category'))]
        if self.user_has_groups('stock.group_production_lot'):
            res_filter.append(('lot', _('One Lot/Serial Number')))
        if self.user_has_groups('stock.group_tracking_lot'):
            res_filter.append(('pack', _('A Pack')))
        return res_filter

    @api.model
    def _selection_filter_by_order_type(self):
        """ Get the list of filter allowed according to the options checked
        in 'Settings\Warehouse'. """
        res_filter = [
            ('none', _('All order types')),
            ('customer', _('One Customer Only')),
            ('supplier', _('One Supplier Only')),
            ('mrp', _('One MRP Order Only')),
        ]
        return res_filter

    name = fields.Char(
        'Valuation Reference',
        required=True,
        help="The name of stock valuation operation."
    )
    location_id = fields.Many2one(
        'stock.location',
        'Location',
        required=True,
        default=_default_location_id,
        help='Stock Location'
    )
    include_child_location = fields.Boolean(
        'Include Child Locations',
        default=False,
        help='whether to consider child locations during stock valuation.'
    )
    start_date = fields.Date(
        'Start Date',
        required=True,
        default=_get_first_date,
        help='Start date of stock valuation statistic.'
    )
    end_date = fields.Date(
        'End Date',
        required=True,
        default=_get_last_date,
        help='End date of stock valuation statistic.'
    )
    date = fields.Datetime(
        'Date',
        required=True,
        default=fields.Datetime.now,
        help="Valuation datetime."
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        index=True,
        required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'stock.inventory'),
        help='Current Company'
    )
    filter_by_product = fields.Selection(
        selection='_selection_filter_by_product',
        string='Filter By Product',
        required=True,
        default='none',
        help="If you do an entire inventory, you can choose 'All Products' "
             "and it will prefill the inventory with the current stock.  If "
             "you only do some products (e.g. Cycle Counting) you can choose "
             "'Manual Selection of Products' and the system won't propose "
             "anything.  You can also let the system propose for a single "
             "product / lot /... "
    )
    filter_by_order_type = fields.Selection(
        selection='_selection_filter_by_order_type',
        string='Filter By Order Type',
        required=True,
        default='none',
        help="If you do an entire inventory, you can choose 'All Products' "
             "and it will prefill the inventory with the current stock.  "
             "If you only do some products (e.g. Cycle Counting) you can "
             "choose 'Manual Selection of Products' and the system won't "
             "propose anything.  You can also let the system propose for "
             "a single product / lot /... "
    )
    product_id = fields.Many2one(
        'product.product',
        'Product',
        help="Specify Product to focus your inventory on a particular Product."
    )
    package_id = fields.Many2one(
        'stock.quant.package',
        'Package',
        help="Specify Pack to focus your inventory on a particular Pack."
    )
    lot_id = fields.Many2one(
        'stock.production.lot',
        'Lot/Serial Number',
        copy=False,
        help="Specify Lot/Serial Number to focus your inventory on a "
             "particular Lot/Serial Number."
    )
    category_id = fields.Many2one(
        'product.category',
        'Product Category',
        help="Specify Product Category to focus your inventory on a particular"
             "Category."
    )
    partner_customer_id = fields.Many2one(
        'res.partner',
        'Customer',
        help="Specify Customer."
    )
    partner_supplier_id = fields.Many2one(
        'res.partner',
        'Supplier',
        help="Specify Supplier."
    )
    involved_mrp_order = fields.Many2one(
        'mrp.production',
        'Manufacture order',
        help="Manufacture Order."
    )

    @api.onchange('filter_by_product')
    def onchange_filter_by_product(self):
        if self.filter_by_product != 'product':
            self.product_id = False
        if self.filter_by_product != 'lot':
            self.lot_id = False
        if self.filter_by_product != 'pack':
            self.package_id = False
        if self.filter_by_product != 'category':
            self.category_id = False

    @api.onchange('filter_by_order_type')
    def onchange_filter_by_order_type(self):
        if self.filter_by_order_type != 'customer':
            self.partner_customer_id = False
        if self.filter_by_order_type != 'supplier':
            self.partner_supplier_id = False
        if self.filter_by_order_type != 'mrp':
            self.involved_mrp_order = False

    @api.multi
    def prepare_valuation(self):
        """
            Redirect to wizard of stock valuation report with some selected
            fields from user
        :return:
        """

        ctx = {
            'location_id': self.location_id and self.location_id.id or False,
            'location': self.location_id and self.location_id.name or False,
            'product_id': self.product_id and self.product_id.id or False,
            'partner_customer_id': self.partner_customer_id and
            self.partner_customer_id.id or False,
            'partner_vendor_id': self.partner_supplier_id and
            self.partner_supplier_id.id or False,
            'involved_mrp_order': self.involved_mrp_order and
            self.involved_mrp_order.id or False,
            'category_id': self.category_id and self.category_id.id or False,
            'lot_id': self.lot_id and self.lot_id.id or False,
            'package_id': self.package_id and self.package_id.id or False,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'include_child_location': self.include_child_location,
            'company_id': self.company_id and self.company_id.id or False
        }

        return {
            'name': _('Stock Valuation List'),
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'wizard.stock.valuation.list',
            'context': ctx,
            'target': 'new',
        }
