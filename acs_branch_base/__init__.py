# -*- coding: utf-8 -*-

from . import models

from odoo import api, SUPERUSER_ID

def _set_branch(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        users = env['res.users'].search([])
        for user in users:
            user.branch_id = env.ref('acs_branch_base.acs_main_branch')
            user.branch_ids = [(6,0,[env.ref('acs_branch_base.acs_main_branch').id])]
    except:
        pass

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: