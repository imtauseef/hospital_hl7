# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError

class MedicalRepresentative(models.Model):
    _name = 'medical.representative'
    _description = "Medical Representative"
    _inherits = {
        'res.partner': 'partner_id',
    }
    _inherit = ['mail.thread']

    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete='restrict')
    active = fields.Boolean(string="Active", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('code', '/') == '/':
                values['code'] = self.env['ir.sequence'].next_by_code('medical.representative') or ''
        return super().create(vals_list)

    def action_mr_visit(self):
        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms_medical_representative.action_medical_representative_visit")
        action['domain'] = [('medical_representative_id', '=', self.id)]
        action['context'] = {'default_medical_representative_id': self.id}
        return action


class MedicalVisit(models.Model):
    _name = 'acs.mr.visit'
    _description = 'Medical Visit'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'acs.hms.mixin']

    READONLY_STATES = {'done': [('readonly', True)], 'cancel': [('readonly', True)]}

    name = fields.Char(size=256, string='Name', tracking=True, states=READONLY_STATES, copy=False)
    activity_name = fields.Char('Purpose', required="True", states=READONLY_STATES)
    date_visit = fields.Datetime('Date', default=fields.Datetime.now, states=READONLY_STATES)
    medical_representative_id = fields.Many2one('medical.representative','MR', help="Name of the Mr", required=True, states=READONLY_STATES)
    physician_id = fields.Many2one('hms.physician','Doctor', help="Name of the Doctor", required=True, states=READONLY_STATES)
    state = fields.Selection([
        ('draft','Draft'),
        ('approved','Approved'),
        ('cancelled','Cancelled'),
        ('done','Done')], 'Status', default="draft") 
    remark = fields.Text('Dr Remark', states=READONLY_STATES)
    product_description = fields.Text('Product Description', states=READONLY_STATES)
    sample_line_ids = fields.One2many('hms.sample.line', 'visit_id', 'Sample Lines', states=READONLY_STATES)
    company_id = fields.Many2one('res.company', states=READONLY_STATES, string='Hospital', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            values['name'] = self.env['ir.sequence'].next_by_code('acs.mr.visit') or ''
        return super().create(vals_list)

    def action_approve(self):
        self.date_visit = datetime.now()
        self.state = 'approved'

    def action_done(self):
        self.acs_receive_samples()
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def unlink(self):
        for rec in self:
            if rec.state in ['done']:
                raise UserError(_('Record in done state can not be deleted.'))
        return super(MedicalVisit, self).unlink()

    def acs_get_sample_locations(self):
        if not self.company_id.acs_mr_usage_location_id:
            raise UserError(_('Please define a MR location from where the Products will be received.'))
        if not self.company_id.acs_mr_stock_location_id:
            raise UserError(_('Please define a MR location where the Products will be stored.'))

        dest_location_id  = self.company_id.acs_mr_stock_location_id.id
        source_location_id  = self.company_id.acs_mr_usage_location_id.id
        return source_location_id, dest_location_id

    def acs_receive_samples(self):
        for rec in self:
            source_location_id, dest_location_id = rec.acs_get_sample_locations()
            for line in rec.sample_line_ids.filtered(lambda s: not s.move_id):
                data = {
                    'product': line.product_id, 
                    'qty': line.qty, 
                    'lot_id': line.lot_id and line.lot_id.id or False
                }
                move = self.consume_material(source_location_id, dest_location_id, data)
                line.move_id = move.id


class ACSSampleLine(models.Model):
    _name = "hms.sample.line"
    _description = "Sample Products"

    @api.depends('price_unit','qty')
    def acs_get_total_price(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.price_unit

    name = fields.Char(string='Name',default=lambda self: self.product_id.name)
    product_id = fields.Many2one('product.product', ondelete="restrict", string='Consumable')
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', help='Amount of medication (eg, 250 mg) per dose', domain="[('category_id', '=', product_uom_category_id)]")
    qty = fields.Float(string='Quantity', default=1.0)
    tracking = fields.Selection(related='product_id.tracking', store=True)
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial Number', domain="[('product_id', '=', product_id)]")
    price_unit = fields.Float(related='product_id.list_price', string='Unit Price', readonly=True)
    subtotal = fields.Float(compute=acs_get_total_price, string='Subtotal', readonly=True, store=True)
    move_id = fields.Many2one('stock.move', string='Stock Move')
    physician_id = fields.Many2one('hms.physician', string='Physician')
    department_id = fields.Many2one('hr.department', string='Department')
    visit_id = fields.Many2one('acs.mr.visit', string='Visit')
    medical_representative_id = fields.Many2one('medical.representative', string='MR', help="Name of the Mr")
    date = fields.Date("Date", default=fields.Date.context_today)
    note = fields.Char("Note")

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
