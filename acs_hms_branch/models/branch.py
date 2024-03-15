# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AcsBranch(models.Model):
    _inherit = 'acs.branch'

    appointment_usage_location_id = fields.Many2one('stock.location', domain=[('usage','=','customer')],
        string='Usage Location for Consumed Products in Appointment')
    appointment_stock_location_id = fields.Many2one('stock.location', domain=[('usage','=','internal')], 
        string='Stock Location for Consumed Products in Appointment')