# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

import operator
import re
from os.path import isfile

from odoo import api, fields, models, tools
from odoo.modules import get_module_resource
from odoo.osv import expression


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    theme_icon = fields.Char(string='Theme Icon Path')
    theme_icon_data = fields.Binary(string='Theme Icon Image', attachment=True)

    @api.model
    def _get_current_theme(self):
        current_theme = self.env['ir.web.theme'].get_current_theme()
        if not current_theme:
            current_theme = self.env['ir.web.theme'].get_default_theme().id
        if not isinstance(current_theme, int):
            current_theme = int(current_theme)
        return self.env['ir.web.theme'].browse(current_theme)

    @api.model_create_multi
    def create(self, vals_list):
        icon_type = self._get_current_theme().base_menu_icon
        self.clear_caches()
        if icon_type == '3d_icon':
            for values in vals_list:
                icon_path = ''
                if values.get('web_icon'):
                    icon = values.get('web_icon').split(',')
                    module_name = icon[0]
                    icon_path = "allure_backend_theme,static/src/img/menu/%s.png" %(module_name)
                if 'web_icon' in values:
                    values['theme_icon_data'] = self._compute_web_icon_data(icon_path or values.get('web_icon'))
        elif icon_type == '2d_icon':
            for values in vals_list:
                icon_path = ''
                if values.get('web_icon'):
                    icon = values.get('web_icon').split(',')
                    module_name = icon[0]
                    icon_path = "allure_backend_theme,static/src/img/menu_2d/%s.png" %(module_name)
                if 'web_icon' in values:
                    values['theme_icon_data'] = self._compute_web_icon_data(icon_path or values.get('web_icon'))
        else:
            for values in vals_list:
                values['theme_icon_data'] = self._compute_web_icon_data(values.get('web_icon'))
        return super(IrUiMenu, self).create(vals_list)

    def write(self, values):
        self.clear_caches()
        if 'theme_icon' in values:
            values['theme_icon_data'] = self._compute_web_icon_data(values['theme_icon'])
        return super(IrUiMenu, self).write(values)

    @api.model
    @tools.ormcache_context('self._uid', keys=('lang',))
    def load_menus_root(self):
        fields = ['name', 'sequence', 'parent_id', 'action', 'web_icon_data']
        menu_roots = self.get_user_roots()
        menu_roots_data = menu_roots.read(fields) if menu_roots else []

        menu_root = {
            'id': False,
            'name': 'root',
            'parent_id': [-1, ''],
            'children': menu_roots_data,
            'all_menu_ids': menu_roots.ids,
        }

        xmlids = menu_roots._get_menuitems_xmlids()
        for menu in menu_roots_data:
            menu['xmlid'] = xmlids[menu['id']]

        return menu_root

    @api.model
    @tools.ormcache_context('self._uid', 'debug', keys=('lang',))
    def load_menus(self, debug):
        """ Loads all menu items (all applications and their sub-menus).

        :return: the menu root
        :rtype: dict('children': menu_nodes)
        """
        icon_type = self._get_current_theme().base_menu_icon
        fields = ['name', 'sequence', 'parent_id', 'action', 'web_icon', 'web_icon_data', 'theme_icon', 'theme_icon_data']
        menu_roots = self.get_user_roots()
        menu_roots_data = menu_roots.read(fields) if menu_roots else []
        menu_root = {
            'id': False,
            'name': 'root',
            'parent_id': [-1, ''],
            'children': [menu['id'] for menu in menu_roots_data],
        }

        all_menus = {'root': menu_root}

        if not menu_roots_data:
            return all_menus

        # menus are loaded fully unlike a regular tree view, cause there are a
        # limited number of items (752 when all 6.1 addons are installed)

        menus_domain = [('id', 'child_of', menu_roots.ids)]
        blacklisted_menu_ids = self._load_menus_blacklist()
        if blacklisted_menu_ids:
            menus_domain = expression.AND([menus_domain, [('id', 'not in', blacklisted_menu_ids)]])
        menus = self.search(menus_domain)
        menu_items = menus.read(fields)
        xmlids = (menu_roots + menus)._get_menuitems_xmlids()

        # add roots at the end of the sequence, so that they will overwrite
        # equivalent menu items from full menu read when put into id:item
        # mapping, resulting in children being correctly set on the roots.
        menu_items.extend(menu_roots_data)

        # set children ids and xmlids
        menu_items_map = {menu_item["id"]: menu_item for menu_item in menu_items}
        for menu_item in menu_items:
            menu_item.setdefault('children', [])
            parent = menu_item['parent_id'] and menu_item['parent_id'][0]
            menu_item['xmlid'] = xmlids.get(menu_item['id'], "")
            if parent in menu_items_map:
                menu_items_map[parent].setdefault(
                    'children', []).append(menu_item['id'])
        all_menus.update(menu_items_map)

        # sort by sequence
        for menu_id in all_menus:
            all_menus[menu_id]['children'].sort(key=lambda id: all_menus[id]['sequence'])

        # recursively set app ids to related children
        def _set_app_id(app_id, menu):
            menu['app_id'] = app_id
            for child_id in menu['children']:
                _set_app_id(app_id, all_menus[child_id])

        for app in menu_roots_data:
            app_id = app['id']
            _set_app_id(app_id, all_menus[app_id])

        # filter out menus not related to an app (+ keep root menu)
        all_menus = {menu['id']: menu for menu in all_menus.values() if menu.get('app_id')}
        all_menus['root'] = menu_root
        # return self.load_web_menus(all_menus, debug)
        menus = menu_items
        icon_type = self._get_current_theme().base_menu_icon
        # load_menus = self.load_menus(debug)
        # for menu in all_menus.values():
        #     webIcon = menu.get('web_icon', '')
        #     webIconlist = webIcon and webIcon.split(',')
        #     iconClass = color = backgroundColor = None
        #     if webIconlist:
        #         if len(webIconlist) >= 2:
        #             iconClass, color = webIconlist[:2]
        #         if len(webIconlist) == 3:
        #             backgroundColor = webIconlist[2]
        #     # if menu['id'] and all_menus[menu['id']]:
        #     if menu['id'] and all_menus[menu['id']] and all_menus[menu['id']].get('theme_icon_data'):
        #         menu['webIconData'] = re.sub(r'\s/g', "", ('data:image/png;base64,%s' % all_menus[menu['id']].get('theme_icon_data').decode('utf-8')))
        #     elif backgroundColor is None and not menu['id']:
        #         if icon_type == '3d_icon':
        #             menu['webIconData'] = '/allure_backend_theme/static/src/img/menu/custom.png'
        #         elif icon_type == '2d_icon':
        #             menu['webIconData'] = '/allure_backend_theme/static/src/img/menu_2d/custom.png'
        #         else:
        #             menu['webIconData'] = '/allure_backend_theme/static/src/img/no_modul_ioc.png'
        return all_menus

    @api.model
    def icon_menu_chnange(self, form_values):
        modules = self.env['ir.module.module'].sudo().search([])
        ctx = self.env.context.copy()
        ctx.update({'ir.ui.menu.full_list': True})
        menu_ids = self.with_context(ctx).sudo().search([('parent_id', '=', False)]).mapped('id')
        board_id = self.env.ref('base.menu_board_root').id
        menu_ids.append(board_id)
        menus = self.sudo().browse(menu_ids)
        icon_type = form_values.get('base_menu_icon')
        def _set_web_icon(base_menu_icon):
            for module in modules.filtered(lambda m: m.name):
                icon_path = 'static/src/img/%s/%s.png' % (base_menu_icon, module.name)
                module_path = get_module_resource('allure_backend_theme', icon_path)
                if isfile(module_path):
                    module.write({'theme_icon': '/allure_backend_theme/' + icon_path})
                elif module.icon == '/base/static/description/icon.png':
                    module.write({'theme_icon': '/allure_backend_theme/static/src/img/%s/custom.png' % (base_menu_icon)});
                else:
                    module.write({'theme_icon': module.icon})
            for menu in menus.filtered(lambda m: m.web_icon):
                path_info = menu.web_icon.split(',')
                module_name = path_info[0]
                icon_path = 'static/src/img/%s/%s.png' % (base_menu_icon, module_name)
                module_path = get_module_resource('allure_backend_theme', icon_path)
                if isfile(module_path):
                    menu.write({'theme_icon': 'allure_backend_theme,' + icon_path,
                        'theme_icon_data': self._compute_web_icon_data('allure_backend_theme,' + icon_path)})
                elif path_info[0] == '/allure_backend_theme/static/src/img/global_search.png':
                    menu.write({'web_icon': '/allure_backend_theme/static/src/img/global_search.png',
                        'theme_icon': '/allure_backend_theme/static/src/img/global_search.png',
                        'theme_icon_data':self._compute_web_icon_data('/allure_backend_theme/static/src/img/global_search.png')})
                elif path_info[0] != '/allure_backend_theme/static/src/img/global_search.png' and path_info[1] == '/base/static/description/icon.png':
                    menu.write({'theme_icon': 'allure_backend_theme,static/src/img/%s/custom.png' % (base_menu_icon),
                        'theme_icon_data':self._compute_web_icon_data('allure_backend_theme,static/src/img/%s/custom.png' % (base_menu_icon))})
                else:
                    menu.write({'theme_icon': menu.web_icon,
                        'theme_icon_data':self._compute_web_icon_data(menu.web_icon)})
                    menu.write({'theme_icon': menu.web_icon,
                        'web_icon_data':self._compute_web_icon_data(menu.web_icon)})
                if path_info[0] == 'base':
                    icon_name = path_info[1].split('/')
                    if icon_name and icon_name[-1:][0]:
                        icon = icon_name[-1:][0]
                        icon_path = "allure_backend_theme,static/src/img/%s/%s" %(base_menu_icon, icon)
                        menu.write({'theme_icon': icon_path,
                            'theme_icon_data': self._compute_web_icon_data(icon_path)})
            if not base_menu_icon:
                for module in modules:
                    path_info = module.icon
                    # path_info.replace('.svg', '.png')
                    module.write({'theme_icon': path_info})
                for menu in menus:
                    if isinstance(menu.web_icon, str):
                        menu.web_icon = menu.web_icon.replace('.svg', '.png')
                    if menu.web_icon:
                        path_info = menu.web_icon
                        menu.write({'theme_icon': path_info,
                            'theme_icon_data': self._compute_web_icon_data(path_info)})

        _set_web_icon(form_values.get('base_menu_icon', False) and\
            form_values['base_menu_icon'] == "3d_icon" and "menu" or\
            form_values['base_menu_icon'] == "2d_icon" and "menu_2d" or False)

        return True

    def load_web_menus(self, debug):
        menus = super(IrUiMenu, self).load_web_menus(debug)
        icon_type = self._get_current_theme().base_menu_icon
        load_menus = self.load_menus(debug)
        for menu in menus.values():
            webIcon = menu.get('webIcon', '')
            webIconlist = webIcon and webIcon.split(',')
            iconClass = color = backgroundColor = None
            if webIconlist:
                if len(webIconlist) >= 2:
                    iconClass, color = webIconlist[:2]
                if len(webIconlist) == 3:
                    backgroundColor = webIconlist[2]
            if icon_type in ['3d_icon', '2d_icon'] and load_menus[menu['id']] and load_menus[menu['id']].get('theme_icon_data'):
                menu['webIconData'] = load_menus[menu['id']].get('theme_icon_data')
            elif backgroundColor is None and not load_menus[menu['id']] and load_menus[menu['id']].get('web_icon_data'):
                if icon_type == '3d_icon':
                    menu['webIconData'] = '/allure_backend_theme/static/src/img/menu/custom.png'
                elif icon_type == '2d_icon':
                    menu['webIconData'] = '/allure_backend_theme/static/src/img/menu_2d/custom.png'
                else:
                    menu['webIconData'] = '/allure_backend_theme/static/src/img/no_modul_ioc.png'
        return menus