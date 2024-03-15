# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AcsLaboratoryRequest(models.Model):
    _inherit = 'acs.laboratory.request'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id, states=STATES)

    def prepare_test_result_data(self, line, patient):
        res = super(AcsLaboratoryRequest, self).prepare_test_result_data(line, patient)
        res['branch_id'] = self.branch_id and self.branch_id.id or False
        return res

    def prepare_sample_data(self, line, patient):
        res = super(AcsLaboratoryRequest, self).prepare_sample_data(line, patient)
        res['branch_id'] = self.branch_id and self.branch_id.id or False
        return res


class PatientLaboratoryTest(models.Model):
    _inherit = 'patient.laboratory.test'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id, states=STATES)
    
    #Give first preference to branch locations
    def acs_get_consume_locations(self):
        source_location_id, dest_location_id = super(PatientLaboratoryTest, self).acs_get_consume_locations()
        if self.branch_id and self.branch_id.laboratory_usage_location_id:
            dest_location_id  = self.branch_id.laboratory_usage_location_id.id
        if self.branch_id and self.branch_id.laboratory_stock_location_id:
            source_location_id  = self.branch_id.laboratory_stock_location_id.id
        return source_location_id, dest_location_id


class AcsLaboratorySample(models.Model):
    _inherit = 'acs.patient.laboratory.sample'

    @api.model
    def _get_branch_id(self):
        branch_id = False
        if self.env.user.branch_id:
            if self.env.user.acs_main_active_branch_id:
                branch_id = self.env.user.acs_main_active_branch_id
            else:
                branch_id = self.env.user.acs_main_active_branch_id or self.env.user.branch_id.id
        return branch_id

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    branch_id = fields.Many2one('acs.branch', string="Branch", default=_get_branch_id, states=STATES)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: