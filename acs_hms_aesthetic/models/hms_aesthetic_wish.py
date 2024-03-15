# -*- coding: utf-8 -*-

from odoo import api, fields, models ,_
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


class AcsAestheticPatientWish(models.Model):
    _name="acs.aesthetic.patient.wish"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'acs.hms.mixin', 'acs.documnt.view.mixin']
    _description = "Aesthetic Patient Wish"
    _order = "id desc"

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    def _get_document_preview_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            rec.document_preview_url = base_url + "/my/acs/image/%s/%s" % (self._name,rec.id)

    def _acs_attachemnt_count(self):
        AttachmentObj = self.env['ir.attachment']
        for rec in self:
            attachments = AttachmentObj.search([
                ('res_model', '=', self._name),
                ('res_id', '=', rec.id)])
            rec.attachment_ids = [(6,0,attachments.ids)]
            rec.attach_count = len(attachments.ids)

    name = fields.Char(string="Name", states=STATES)
    patient_id = fields.Many2one('hms.patient', string='Patient', required=True, states=STATES)
    physician_id = fields.Many2one('hms.physician', ondelete='restrict', string='Physician', 
        index=True, states=STATES)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status', default='draft')
    company_id = fields.Many2one('res.company', ondelete='restrict', states=STATES,
        string='Hospital', default=lambda self: self.env.company)
    date = fields.Datetime("Date", default=fields.Datetime.now)
    treatment_id = fields.Many2one('hms.treatment', 'Treatment', states=STATES)
    note = fields.Text("Notes", states=STATES)

    #BODY TREATMENT PLAN
    cellulitis = fields.Boolean(string="Cellulitis", states=STATES)
    stretch_marks = fields.Boolean(string="Stretch Marks", states=STATES)
    body_circumference_reduction = fields.Boolean(string="Body Circumference Reduction", states=STATES)
    adiposity = fields.Boolean(string="Adiposity (Rabbits, Chubby, Llanticas)", states=STATES)
    hair_removal = fields.Boolean(string="Hair Removal", states=STATES)
    definitive_hair_removal = fields.Boolean(string="Definitive Hair Removal", states=STATES)
    dehydrated_skin = fields.Boolean(string="Dehydrated Skin", states=STATES)
    overweight = fields.Boolean(string="Overweight", states=STATES)
    skin_faccidity = fields.Boolean(string="Skin Flaccidity", states=STATES)
    prepost_operative = fields.Boolean(string="Pre-post Operative", states=STATES)
    postpartum_treatments = fields.Boolean(string="Postpartum treatments", states=STATES)
    body_description = fields.Text(string="Other Body Description", states=STATES)
    
    body_treatment_product_ids = fields.Many2many('product.product', 'body_patient_wish_treatment_product_ids_rel', 'wish_id', 'product_id', 'Body Treatments', states=STATES)
    body_nutrition_product_ids = fields.Many2many('product.product', 'body_patient_wish_nutrition_product_ids_rel', 'wish_id', 'product_id', 'Body Nutrition', states=STATES)
    body_upkeep_product_ids = fields.Many2many('product.product', 'body_patient_wish_upkeep_product_ids_rel', 'wish_id', 'product_id', 'Body Upkeep', states=STATES)

    #FACIAL TREATMENT PLAN
    scars = fields.Boolean(string="Acne / Scars", states=STATES)
    pigmentation = fields.Boolean(string="Pigmentation", states=STATES)
    expression_lines = fields.Boolean(string="Expression lines", states=STATES)
    wrinkles = fields.Boolean(string="Wrinkles", states=STATES)
    spots = fields.Boolean(string="Spots", states=STATES)
    flaccidity = fields.Boolean(string="Flaccidity", states=STATES)
    facial_description = fields.Text(string="Other Facial Description", states=STATES)

    facial_treatment_product_ids = fields.Many2many('product.product', 'facial_patient_wish_treatment_product_ids_rel', 'wish_id', 'product_id', 'Facial Treatments', states=STATES)
    facial_nutrition_product_ids = fields.Many2many('product.product', 'facial_patient_wish_nutrition_product_ids_rel', 'wish_id', 'product_id', 'Facial Nutrition', states=STATES)
    facial_upkeep_product_ids = fields.Many2many('product.product', 'facial_patient_wish_upkeep_product_ids_rel', 'wish_id', 'product_id', 'Facial Upkeep', states=STATES)

    attach_count = fields.Integer(compute="_acs_attachemnt_count", readonly=True, string="Documents")
    attachment_ids = fields.Many2many('ir.attachment', 'attachment_patient_wish_rel', 'treatment_id', 'attachment_id', compute="_acs_attachemnt_count", string="Attachments")
    document_preview_url = fields.Char(compute=_get_document_preview_url, string="Document Preview Link")

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def unlink(self):
        for rec in self:
            if rec.state not in ['cancel']:
                raise UserError(_('Record can be deleted only in Canceled state.'))
        return super(AcsAestheticPatientWish, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            values['name'] = self.env['ir.sequence'].next_by_code('acs.aesthetic.patient.wish') or 'New Aesthetic Patient Wish'
        return super().create(vals_list)

    def create_procedure(self, products, treatment):
        Procedure = self.env['acs.patient.procedure']
        base_date = fields.Datetime.from_string(fields.Datetime.now())
        for product in products:
            if not product.product_tmpl_id.product_procedure_line_ids:
                Procedure.create({
                    'patient_id': treatment.patient_id.id,
                    'physician_id': treatment.physician_id and treatment.physician_id.id or False,
                    'product_id': product.id,
                    'treatment_id': treatment.id,
                })
            else:
                for line in product.product_tmpl_id.product_procedure_line_ids:
                    for count in range(0,line.repeat_for):
                        Procedure.create({
                            'patient_id': treatment.patient_id.id,
                            'physician_id': treatment.physician_id and treatment.physician_id.id or False,
                            'product_id': line.product_id.id,
                            'treatment_id': treatment.id,
                            'date': (base_date + timedelta(days=line.days_to_add)),
                        })

    def action_create_treatement(self):
        department = self.env['hr.department'].search([('department_type','=','aesthetic')], limit=1)
        treatment = self.env['hms.treatment'].create({
            'patient_id': self.patient_id.id,
            'physician_id': self.physician_id.id,
            'department_id': department.id if department else False,
            'aesthetic_wish_id': self.id,
        })
        body_treatments = self.body_treatment_product_ids + self.body_nutrition_product_ids + self.body_upkeep_product_ids
        self.create_procedure(body_treatments, treatment)
        facial_treatments = self.facial_treatment_product_ids + self.facial_nutrition_product_ids + self.facial_upkeep_product_ids
        self.create_procedure(facial_treatments, treatment)

        action = self.env["ir.actions.actions"]._for_xml_id("acs_hms_aesthetic.action_acs_treatment")
        action['context'] = {'default_patient_id': self.patient_id.id, 'default_physician_id': self.physician_id.id}
        action['views'] = [(self.env.ref('acs_hms.view_hospital_hms_treatment_form').id, 'form')]
        action['res_id'] = treatment.id
        self.treatment_id = treatment.id
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: