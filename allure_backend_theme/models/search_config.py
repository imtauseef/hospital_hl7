# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

import numbers

from odoo import models, api, fields
from odoo.exceptions import AccessError
from lxml import etree, html

NEGATIVE_TERMS = ('False', ' ', 'None', False, None)


class GlobalSearchConfigTemplate(models.Model):
	_name = 'global.search.config.template'
	_rec_name = 'model_id'
	_description = 'Global Search Configuration Template'

	model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete="cascade",domain="[('access_ids.id','!=',False),('model','!=','res.users.apikeys.show'),('model','!=','barcode.rule'),('model','!=','account.bank.statement')]")
	field_ids = fields.Many2many('ir.model.fields', string='Fields',
								 domain="[('model_id', '=', model_id), ('name', '!=', 'id'), ('ttype', '!=', 'boolean'),('store','=','True'),('ttype','!=','binary'),('related','=',False),('compute','=',False),('name','!=','totp_secret'),('name','!=','group_id')]",
								 required=True)

	_sql_constraints = [('uniq_model', "UNIQUE(model_id)", "The Model must be unique!")]

	def _get_global_search_config_template_domain(self):
		models = self.env['ir.model'].search([('state', '!=', 'manual'), ('transient', '=', False)])
		access_model = self.env['ir.model.access']
		model_ids = [model.id for model in models if access_model.with_user(
				user=self.env.user.id
			).check(model.model, 'read', raise_exception=False)]
		return [('model_id', 'in', model_ids)]

	@api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		context = dict(self.env.context or {})
		if context.get('global_search_config'):
			args = (args or []) + self._get_global_search_config_template_domain()
		return super(GlobalSearchConfigTemplate, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

	@api.onchange('model_id')
	def _onchange_model_id(self):
		self.field_ids = [(6, 0, [])]

	def apply_changes_in_searches(self):
		""" Its calling for effects on searches."""
		searches = self.env['global.search.config'].search([('batch_id', '=', False), ('template_id', 'in', self.ids)])
		for rec in searches.filtered(lambda s: not s.customized):
			rec.set_values_template_batch(rec.template_id)
		return True


class GlobalSearchConfig(models.Model):
	_name = 'global.search.config'
	_rec_name = 'model_id'
	_description = 'Global Search Configuration'

	template_id = fields.Many2one('global.search.config.template',
		string="Template") #domain="[('id', in, [])]"
	batch_id = fields.Many2one('global.search.config.batch', string="Batch")
	user_id = fields.Many2one('res.users', string='User',
		default=lambda self: self.env.user, copy=False)
	customized = fields.Boolean(string="Customized")
	model_id = fields.Many2one('ir.model', string="Model", required=True, ondelete="cascade",domain="[('access_ids.id','!=',False),('model','!=','res.users.apikeys.show'),('model','!=','barcode.rule'),('model','!=','account.bank.statement')]")
	field_ids = fields.Many2many('ir.model.fields', string="Fields",
		domain="[('model_id', '=', model_id), ('name', '!=', 'id'),('store','=','True'),('ttype','!=','binary'),('related','=',False),('compute','=',False),('name','!=','totp_secret'),('name','!=','group_id')]",
		required=True) #order="ir_model_fields_id.field_description desc"

	_sql_constraints = [
		('uniq_template_user',
		 "UNIQUE(template_id, user_id)", "The template must be unique per user!"),
	]

	def write(self, vals):
		'''Override to manage customized boolean'''
		if 'customized' not in vals and ((vals.get('user_id') and len(vals.keys()) > 1) or not vals.get('user_id')):
			vals['customized'] = True
		if 'template_id' in vals and not vals.get('model_id', False):
			vals['model_id'] = self.env['global.search.config.template'].search([('id', '=', vals['template_id'])]).model_id.id
		return super(GlobalSearchConfig, self).write(vals)

	@api.model
	def create(self, vals):
		'''Override check the values'''
		if 'template_id' in vals and not vals.get('model_id', False):
			vals['model_id'] = self.env['global.search.config.template'].search([('id', '=' ,vals['template_id'])]).model_id.id
		return super(GlobalSearchConfig, self).create(vals)

	@api.onchange('template_id')
	def _onchange_template_id(self):
		'''To set fields as per template selection.'''
		for rec in self:
			rec.set_values_template_batch(rec.template_id)

	@api.onchange('model_id')
	def _onchange_model_id(self):
		if self.template_id:
			self._onchange_template_id()
		else:
			self.field_ids = [(6, 0, [])]

	def set_values_template_batch(self, template_batch_id):
		self.ensure_one()
		self.field_ids = [(6, 0, template_batch_id.field_ids.ids)]
		self.model_id = template_batch_id.model_id.id
		self.customized = False

	def set_default_template_batch(self):
		'''Set default button.
		To set fields as per template or batch selection. '''
		for rec in self:
			rec.set_values_template_batch(rec.batch_id or rec.template_id)

	def _get_search_more_config(self, kw):
		return dict(
			limit=kw['limit'],
			offset=(kw['searched_datas'] + kw['offset']),
			total=kw['total'],
			remaining=max(0, (kw['total'] - (kw['offset'] + kw['limit'])))
		)

	def _process_global_search_data(self, kwargs):
		# this method is unnecessary for odoo v15
		# with api.Environment.manage():
			# As this function is in a new thread, need to open a new cursor, because the old one may be closed
		new_cr = self.pool.cursor()
		self = self.with_env(self.env(cr=new_cr))
		# search data with handling access error
		try:
			kwargs['search_more_options']['total'] = self.env[kwargs['model']].search_count(kwargs['dom'])
			datas = self.env[kwargs['model']].search_read(kwargs['dom'], list(kwargs['fields'].keys()) + ['display_name'],
				offset=kwargs['search_more_options']['offset'], limit=kwargs['search_more_options']['limit'])
			kwargs['search_more_options']['searched_datas'] = len(datas)
			options = self._get_search_more_config(kwargs['search_more_options'])
			for data in datas:
				for f, v in list(data.items()):
					if f in ['display_name', 'id']:
						continue
					if type(v) is list:
						if data[f]:
							x2m_data = self.env[kwargs['fields'][f][1]].browse(data[f]).name_get()
							x2m_v = ', '.join([d[1] for d in x2m_data if kwargs['search_string'].lower() in d[1].lower()\
								and d[1] not in NEGATIVE_TERMS])
							if x2m_v:
								data[kwargs['fields'][f][0]] = x2m_v
					elif type(v) is tuple:
						if data[f] and data[f][1] and kwargs['search_string'].lower() in data[f][1].lower():
							data[kwargs['fields'][f][0]] = data[f][1]
					else:
						if isinstance(data[f], numbers.Number) and type(data[f]) is not bool:
							data[f] = str(data[f])
						if data[f] and kwargs['search_string'].lower() in str(data[f]).lower():
							data[kwargs['fields'][f][0]] = data[f]
					del data[f]
					if data.get(kwargs['fields'][f][0]) and kwargs['search_string'].lower() not in str(data[kwargs['fields'][f][0]]).lower():
						del data[kwargs['fields'][f][0]]
			# Need to close old cursor
			new_cr.close()
			return [datas, options]
		except AccessError:
			return False
