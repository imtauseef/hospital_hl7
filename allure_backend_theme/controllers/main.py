# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

import threading
import queue
from odoo import _
from odoo.exceptions import UserError
from odoo.exceptions import AccessError

from odoo import http
from odoo.addons.web.controllers.main import *
from odoo.http import request


class MenuSearch(http.Controller):

    @http.route('/all/menu/search', auth='user', type='json')
    def all_visible_menu(self):
        all_menu_ids = request.env['ir.ui.menu'].search([('action', '!=', False)])
        menu_ids = []
        for menu in all_menu_ids:
            parent_path = menu.parent_path
            parent_menu_list = list(map(int, parent_path.split('/')[:-1]))
            parent_menu_ids = request.env['ir.ui.menu'].browse(parent_menu_list)
            if len(parent_menu_list) == len(parent_menu_ids._filter_visible_menus()):
                menu_ids.append(menu.id)
        menu_datas = request.env['ir.ui.menu'].search_read([
            ('id', 'in', menu_ids),
            ('action', '!=', False)],
            ['name', 'action', 'complete_name','parent_path'])
        return menu_datas

    @http.route('/globalsearch/model_fields', type='json', auth="user")
    def search_model_fields(self, **kwargs):
        '''This function prepares values for autocomplete 'Search for <model:name>:'
        it returns Models whose template is assigned to current login user.
        '''
        GS = request.env['global.search.config'].with_user(user=request.env.user.id).search([('user_id', '=', request.env.user.id)])
        result = dict([(gs.model_id.name, gs.model_id.model) for gs in GS if len(gs.field_ids) > 0])
        return result

    @http.route('/globalsearch/search_data', type='json', auth="user")
    def search_data(self, **kwargs):
        '''This function returns data for partucular model's search expand.'''
        que = queue.Queue()
        globalSearchConfig = request.env['global.search.config']
        search_string = kwargs['search_string']
        try:
            search_datas = []
            # .filtered(lambda acid: acid.perm_read)
            # this field list for res.groups model due to group user acess
            field_nme_list = ['recurring_plan','recurring_revenue','recurring_revenue_monthly','recurring_revenue_monthly_prorated','extract_populated_fields']
            for model in kwargs['models']:
                GS = globalSearchConfig.with_user(user=request.env.user.id).search([('user_id', '=', request.env.user.id), ('model_id.model', '=', model)], limit=1)
                model_lst = request.env['ir.model'].with_user(request.env.user.id).search([('model','=',model)])
                access_ids = model_lst.access_ids.check(model, 'read', False)
                if access_ids and GS.field_ids:
                    fields = dict([(field.name, (field.field_description, field.relation)) for field in GS.field_ids.filtered(lambda fid: fid.ttype != 'binary' and fid.store == True and fid.related != '') if field.name not in field_nme_list])
                    dom = ['|' for l in range(len(fields)-1)]
                    dom.extend([(f, 'ilike', kwargs['search_string']) for f in fields.keys()])   
                    kwargs['fields'] = fields
                    kwargs['dom'] = dom
                    kwargs['model'] = model
                    try:
                        val = request.env['ir.model.access'].check(model=kwargs['model'], mode='read', raise_exception=True)
                        thread_process = threading.Thread(target=lambda q, arg: q.put(globalSearchConfig._process_global_search_data(arg)), args=(que, kwargs))
                        if thread_process:
                            thread_process.start()
                            thread_process.join()
                            datas = que.get()
                            if datas:
                                search_datas.append({'model': model, 'datas': datas[0], 'options': datas[1]})
                    except AccessError:
                        continue
            return search_datas #or [{'label': '(no result)'}]
            # return [{'label': '(no result)'}]
        except (KeyError) as e: 
            raise UserError(
                _("Incorrect configuration, please check it.\n\n%s not found") % (e))
            