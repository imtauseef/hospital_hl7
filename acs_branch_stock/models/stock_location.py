# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = 'stock.location'

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

    # @api.constrains('branch_id')
    # def _check_branch(self):
    #     warehouse_obj = self.env['stock.warehouse']
    #     warehouse_id = warehouse_obj.search(
    #         ['|', '|', ('wh_input_stock_loc_id', '=', self.id),
    #          ('lot_stock_id', '=', self.id),
    #          ('wh_output_stock_loc_id', '=', self.id)])
    #     for warehouse in warehouse_id:
    #         if self.branch_id != warehouse.branch_id:
    #             raise UserError(_('Configuration error\nYou  must select same branch on a location as assigned on a warehouse configuration.'))


