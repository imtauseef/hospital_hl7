# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.osv import expression
from odoo.http import request


class IrModel(models.Model):
    _inherit = 'ir.model'

    def _get_global_search_config_domain(self, user):
        models = self.env['ir.model'].search([('state', '!=', 'manual'), ('transient', '=', False),('access_ids','!=','')])
        access_model = self.env['ir.model.access']
        model_ids = [model.id for model in models if access_model.with_user(
                user=user
            ).check(model.model, 'read', raise_exception=False)]
        return [('id', 'in', model_ids)]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('global_search_config', False) and self._context.get('global_search_user_id'):
            args += self._get_global_search_config_domain(self._context['global_search_user_id'])
            args += [('id', 'in', self.search([('transient', '=', False)]).filtered(lambda model: not self.env[model.model]._abstract).ids)]
        return super(IrModel, self).name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        ''' @Override: to restrict models in global search. '''
        domain = domain or []
        if self._context.get('global_search_config', False) and self._context.get('global_search_user_id'):
            user_domain = self._get_global_search_config_domain(self._context['global_search_user_id'])
            domain = expression.AND([domain, user_domain])
        return super(IrModel, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('global_search_config', False):
            args += [
                ('store', '=', True),
                ('ttype', 'not in', ('boolean', 'binary', 'html')),
            ]
        return super(IrModelFields, self).name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        ''' @Override: to restrict models fields in global search. '''
        domain = domain or []
        if self._context.get('global_search_config', False):
            domain = expression.AND([domain, [
                ('store', '=', True),
                ('ttype', 'not in', ('boolean', 'binary', 'html')),
            ]])
        return super(IrModelFields, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        info = super().session_info()
        user = request.env.user
        info["group_global_search_user"] = user.has_group('allure_backend_theme.group_global_search_user')
        return info
        