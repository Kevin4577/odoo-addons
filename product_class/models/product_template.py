# -*- coding: utf-8 -*-
# © 2017 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _
from openerp.exceptions import ValidationError


class ProductTemplate(models.Model):
    "Data model of Product Template."
    _inherit = 'product.template'

    product_stage_id = fields.Many2one('product.stage',
                                       'Product Stage', ondelete='restrict',
                                       help='Product Stage', index=True)
    product_line_id = fields.Many2one('product.line', 'Product Line',
                                      ondelete='restrict',
                                      help='Product Line', index=True)
    product_class_id = fields.Many2one('product.class',
                                       'Product Class', ondelete='restrict',
                                       help='Product Class', index=True)
    product_family_id = fields.Many2one('product.family',
                                        'Product Family', ondelete='restrict',
                                        help='Product Family', index=True)
    customer_product_code = fields.Char('Customer Product Code',
                                        help='Customer Product Code')
    product_ordering_code = fields.Char('Product Ordering Code',
                                        help='Product Ordering Code')
    rd_product_code = fields.Char('R&D Product Code',
                                  help='R&D Product Code')
    rd_drawing_number = fields.Char('R&D Drawing Number',
                                    help='R&D Drawing Number')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)',
                         _('The name of the product must be unique.'))]

    @api.onchange('product_stage_id')
    def onchange_stage(self):
        """To return domain of product line."""
        domain = []
        if self.product_stage_id:
            domain = [('id', 'in', self.product_stage_id.line_ids.ids)]
        return {'domain': {'product_line_id': domain}}

    @api.onchange('product_line_id')
    def onchange_line(self):
        """To set product stage based on product line and return domain
        of product class."""
        class_domain = []
        stage_domain = []
        if self.product_line_id:
            if (self.product_stage_id.id not in
                    self.product_line_id.stage_ids.ids):
                self.product_stage_id = False
            stage_domain = [('id', 'in',
                             self.product_line_id.stage_ids.ids)]
            class_domain = [('id', 'in', self.product_line_id.class_ids.ids)]
        return {'domain': {'product_class_id': class_domain,
                           'product_stage_id': stage_domain}}

    @api.onchange('product_class_id')
    def onchange_class(self):
        """To set product line based on product class and return domain
        of product family."""
        line_domain = []
        family_domain = []
        if self.product_class_id:
            if (self.product_line_id.id
                    not in self.product_class_id.line_ids.ids):
                self.product_line_id = False
            line_domain = [('id', 'in',
                            self.product_class_id.line_ids.ids)]
            family_domain = [('id', 'in',
                              self.product_class_id.family_ids.ids)]
        return {'domain': {'product_family_id': family_domain,
                           'product_line_id': line_domain}}

    @api.onchange('product_family_id')
    def onchange_family(self):
        """To set product class based on product family."""
        domain = []
        if self.product_family_id:
            if (self.product_class_id.id
                    not in self.product_family_id.class_ids.ids):
                self.product_class_id = False
            domain = [('id', 'in', self.product_family_id.class_ids.ids)]
        return {'domain': {'product_class_id': domain}}

    @api.multi
    def generate_product_code(self):
        """To Generate product code based on sequence."""
        seq_obj = self.env['ir.sequence']
        for product in self:
            if not product.default_code:
                if not product.product_stage_id:
                    raise ValidationError(_("Please select product stage."))
                if not product.product_line_id:
                    raise ValidationError(_("Please select product line."))
                if not product.product_class_id:
                    raise ValidationError(_("Please select product class."))
                if not product.product_family_id:
                    raise ValidationError(_("Please select product family."))
                prefix = product.product_stage_id.code + \
                    product.product_line_id.code + \
                    product.product_class_id.code + \
                    product.product_family_id.code
                seq_cnt = seq_obj.search([('prefix', '=', prefix)], count=True)
                if seq_cnt < 1:
                    seq_obj.create({
                        'name': product.product_stage_id.name + '-' +
                        product.product_line_id.name + '-' +
                        product.product_class_id.name + '-' +
                        product.product_family_id.name,
                        'code': prefix,
                        'prefix': prefix,
                        'company_id': False,
                        'padding': 4,
                        'number_increment': 1,
                    })
                product.default_code = seq_obj.next_by_code(prefix)
        return True
