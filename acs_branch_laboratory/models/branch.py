# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AcsBranch(models.Model):
    _inherit = 'acs.branch'

    laboratory_usage_location_id = fields.Many2one('stock.location', domain=[('usage','=','customer')],
        string='Usage Location for Consumed Products in laboratory')
    laboratory_stock_location_id = fields.Many2one('stock.location', domain=[('usage','=','internal')], 
        string='Stock Location for Consumed Products in laboratory')