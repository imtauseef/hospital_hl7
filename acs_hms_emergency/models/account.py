# -*- coding: utf-8 -*-

from odoo import api,fields,models,_


class AccountMove(models.Model):
    _inherit = 'account.move'

    emergency_id = fields.Many2one('acs.hms.emergency',  string='Emergency', readonly=True, states={'draft': [('readonly', False)]})
    hospital_invoice_type = fields.Selection(selection_add=[('emergency', 'Emergency')])
