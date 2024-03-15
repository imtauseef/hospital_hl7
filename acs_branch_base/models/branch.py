# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AcsBranch(models.Model):
    _name = 'acs.branch'
    _description = 'Company Branch'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    currency_id = fields.Many2one('res.currency', string="Currency")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone No")
    address = fields.Text("Address")
