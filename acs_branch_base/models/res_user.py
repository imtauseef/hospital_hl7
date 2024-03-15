# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.http import request


class AcsUsers(models.Model):
    _inherit = 'res.users'

    def _get_default_branch(self):
        branch = False
        try:
            branch =self.env.ref('acs_branch_base.acs_main_branch')
        except:
            pass
        return branch

    def _get_default_allowed_branch(self):
        branch = False
        try:
            branch =self.env.ref('acs_branch_base.acs_main_branch')
        except:
            pass
        return branch

    branch_ids = fields.Many2many('acs.branch', 'acs_user_id', 'acs_branch_id', 'branch_user_id', string="Allowed Branches", default=_get_default_allowed_branch)
    branch_id = fields.Many2one('acs.branch', string='Branch', default=_get_default_branch)
    acs_active_branch_ids = fields.Many2many('acs.branch', 'acs_user_active_branch_rel', 'acs_branch_id', 'branch_user_id', string="Active Branches")
    acs_main_active_branch_id = fields.Many2one('acs.branch', string="Main Active Branch")

    @api.onchange('branch_ids')
    def acs_onchange_branch(self):
        self.acs_active_branch_ids = [(6,0,[])]
        self.acs_main_active_branch_id = False

    def write(self, values):
        if 'branch_id' in values or 'branch_ids' in values:
            self.env['ir.model.access'].call_cache_clearing_methods()
            self.env['ir.rule'].clear_caches()
            #self.has_group.clear_cache(self)
        user = super(AcsUsers, self).write(values)
        return user

    #ACS: To Fix issue of cache updated it manually
    @api.model
    def acs_clean_rule_cache(self, branches=[], main_branch=False):
        if branches or main_branch:
            self.env.user.sudo().write({'acs_active_branch_ids': [(6,0,branches)], 'acs_main_active_branch_id': main_branch})
        self.env['ir.rule'].with_context(allowed_branch_ids=branches).clear_caches()

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['branch_id']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['branch_id']
