# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

import datetime
from odoo.osv import expression
from odoo import fields, models, api, modules
from odoo.modules import get_module_resource


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _get_global_search_user_domain(self, model):
        access_model = self.env['ir.model.access']
        user_ids = []
        for user in self.search([]):
            if access_model.with_user(user=user.id).check(model, 'read', raise_exception=False):
                user_ids.append(user.id)
        return [('id', 'in', user_ids)]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('global_search_model'):
            args += self._get_global_search_user_domain(self._context['global_search_model'])
        return super(ResUsers, self).name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        ''' @Override: to restrict users in global search batches. '''
        domain = domain or []
        if self._context.get('global_search_model'):
            user_domain = self._get_global_search_user_domain(self._context['global_search_model'])
            domain = expression.AND([domain, user_domain])
        return super(ResUsers, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    display_density = fields.Selection([
                ('default', 'Default'),
                ('comfortable', 'Comfortable'),
                ('compact', 'Compact'),
            ], string="Display Density", default='default')
    tab_type = fields.Selection([
                ('horizontal_tabs', 'Horizontal Tabs'),
                ('vertical_tabs', 'Vertical Tabs'),
            ], string="Tab Type", default='vertical_tabs')
    tab_configration = fields.Selection([
                ('open_tabs','Open Tabs'),
                ('close_tabs','Close Tabs',),
            ], string="Tab Config.", default='open_tabs')
    base_menu =  fields.Selection([
                ('base_menu','Horizontal Menu'),
                ('theme_menu','Vertical Menu'),
            ], string="Menu", default='theme_menu')
    font_type_values =  fields.Selection([
                ('roboto','Roboto'),
                ('open_sans','Open Sans'),
                ('alice','Alice'),
                ('abel','Abel'),
                ('montserrat','Montserrat'),
                ('lato','Lato'),
            ], string="Font", default='roboto')
    box_type = fields.Selection([
                ('curved_graph', 'Curved Graph'),
                ('boxed_graph', 'Boxed Graph'),
            ], string="Graph Type", default='curved_graph')
    radio_type = fields.Selection([
        ('radio_circle_normal', 'Radio1'),
        ('radio_circle_middle', 'Radio2'),
        ('radio_circle_full', 'Radio3'),
        ('radio_squre_circle', 'Radio4'),
        ('radio_squre_full', 'Radio5')
        ], string="Radio Type", default='radio_circle_normal')
    mode = fields.Selection([
        ('light_mode_on', 'Light'),
        ('night_mode_on', 'Night'),
        ('normal_mode_on', 'Normal'),
        ], string="Mode", default='normal_mode_on')

    @api.model
    def get_users_themes(self):
        return self.search_read([('share', '=', False)], [
            'display_density','tab_type','tab_configration',
            'base_menu','font_type_values','mode','box_type','radio_type',
        ])

    def get_module_theme_icon(self, module):
        icon = module + '.png'
        current_theme = self.env['ir.web.theme'].get_current_theme()
        theme_type = self.env['ir.web.theme'].browse(int(current_theme))
        if theme_type.base_menu_icon == '3d_icon':
            iconpath = ['static', 'src', 'img', 'menu', icon]
        elif theme_type.base_menu_icon == '2d_icon':
            iconpath = ['static', 'src', 'img', 'menu_2d', icon]
        else:
            return modules.module.get_module_icon(module)
        if modules.module.get_module_resource(module, *iconpath):
            return ('/' + 'allure_backend_theme' + '/') + '/'.join(iconpath)
        return '/allure_backend_theme/'  + '/'.join(iconpath)

    @api.model
    def systray_get_activities(self):
        res = super(ResUsers, self).systray_get_activities()
        for resList in res:
            module = self.env[resList['model']]._original_module
            icon = module and self.get_module_theme_icon(module)
            resList['icon'] = icon
        return res