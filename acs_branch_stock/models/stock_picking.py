# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

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