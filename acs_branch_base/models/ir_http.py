# -*- coding: utf-8 -*-

from odoo import api, models,_
from odoo.http import request
from odoo.exceptions import AccessError


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super(IrHttp, self).session_info()
        user = request.env.user
        if self.env.user.has_group('base.group_user'):
            session_info.update({
                # current_branch should be default_branch
                "user_branches": {
                    'current_branch': user.branch_id.id,
                    'allowed_branches': {
                        bran.id: {
                            'id': bran.id,
                            'name': bran.name,
                        } for bran in user.branch_ids
                    },
                },
                "show_effect": True,
                "display_switch_branch_menu": user.has_group('acs_branch_base.group_multi_branch') and len(user.branch_ids) > 1,
            })
            self.env['ir.rule'].clear_caches()
        return session_info


class IrRule(models.Model):
    _inherit = 'ir.rule'

    #Pass branch to compute in Rule.
    @api.model
    def _eval_context(self):
        res = super(IrRule, self)._eval_context()
        branch_ids = self.env.context.get('allowed_branch_ids', [])
        if not branch_ids:
            branch_ids = self.env.user.sudo().acs_active_branch_ids.ids

        if not branch_ids:
            branch_ids = self.env.user.branch_ids.ids
        if not self.env.su:
            user_branch_ids = self.env.user.branch_ids.ids
            if any((bid and bid not in user_branch_ids) for bid in branch_ids):
                raise AccessError(_("Access to unauthorized or invalid Branch."))

        res['branch_ids'] = branch_ids
        res['branch_id'] = branch_ids[0] if branch_ids else 0
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: