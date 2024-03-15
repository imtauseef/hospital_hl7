# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AcsPatientProcedure(models.Model):
    _inherit = 'acs.patient.procedure'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id)

    #Give first preference to branch locations
    def acs_get_consume_locations(self):
        source_location_id, dest_location_id = super(AcsPatientProcedure, self).acs_get_consume_locations()
        if self.branch_id and self.branch_id.appointment_usage_location_id:
            dest_location_id  = self.branch_id.appointment_usage_location_id.id
        if self.branch_id and self.branch_id.appointment_stock_location_id:
            source_location_id  = self.branch_id.appointment_stock_location_id.id
        return source_location_id, dest_location_id


class Appointment(models.Model):
    _inherit = 'hms.appointment'
    
    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id)

    #Give first preference to branch locations
    def acs_get_consume_locations(self):
        source_location_id, dest_location_id = super(Appointment, self).acs_get_consume_locations()
        if self.branch_id and self.branch_id.appointment_usage_location_id:
            dest_location_id  = self.branch_id.appointment_usage_location_id.id

        if self.branch_id and self.branch_id.appointment_stock_location_id:
            source_location_id = self.branch_id.appointment_stock_location_id.id

        return source_location_id, dest_location_id


class ACSPatient(models.Model):
    _inherit = 'hms.patient'

    #Do not set branch by default as all patient shoudl be shared across all branch by default.
    branch_id = fields.Many2one('acs.branch', string="Branch")


class Physician(models.Model):
    _inherit = 'hms.physician'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id)


class ACSTreatment(models.Model):
    _inherit = 'hms.treatment'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id)


class ACSPrescriptionOrder(models.Model):
    _inherit = 'prescription.order'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id)


class ACSHmsMixin(models.AbstractModel):
    _inherit = "acs.hms.mixin"
    _description = "HMS Mixin"

    def acs_prepare_invocie_data(self, partner, patient, product_data, inv_data):
        data = super(ACSHmsMixin, self).acs_prepare_invocie_data(partner, patient, product_data, inv_data)
        if 'branch_id' in self._fields:
            data['branch_id'] = self.branch_id and self.branch_id.id or False
        return data

    def consume_material(self, source_location_id, dest_location_id, product_data):
        move = super(ACSHmsMixin, self).consume_material(source_location_id, dest_location_id, product_data)
        if 'branch_id' in self._fields:
            move.branch_id = self.branch_id and self.branch_id.id or False
        return move