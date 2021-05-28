# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)
from requests import get,post
import json
from datetime import datetime

class hassio_presets(models.Model):
	_name = "hassio.presets"
	
	name = fields.Char('Name')
	entity_id = fields.Many2one('hassio.entity',string="Entity")
	service_data = fields.Text('Service Data')
	service = fields.Many2one('hassio.service',string="Service")
	
	@api.onchange('entity_id')
	def onchange_entity_id(self):
		if self.entity_id:
			return {
				'domain': {
					'service': [('id','in',self.entity_id.services.ids)]
				}
			}
	
	def execute(self):
		
		self.with_context({'service_data': self.service_data, 'entity_id': self.entity_id.name}).service.execute()
		
		
class hassio_entity_type_properties(models.Model):
	_name = "hassio.entity_type.properties"
	
	name = fields.Char('Name')
	ttype = fields.Char("Type")
	default = fields.Char('Default')
	description = fields.Char('Description')
	entity_type_id = fields.Many2one('hassio.entity_type',string="Entity Type")

class hassio_entity_type(models.Model):
	_name = "hassio.entity_type"

	name = fields.Char('Name')
	code = fields.Char("Code")
	properties = fields.One2many('hassio.entity_type.properties','entity_type_id',string="Properties")
	
class hassio_entity(models.Model):
	_name = "hassio.entity"
	
	name = fields.Char('Entity')
	services = fields.Many2many('hassio.service',string="Services")
	friendly_name = fields.Char('Friendly Name')
	ttype = fields.Many2one('hassio.entity_type',string="Type")
	attributes = fields.Text('Attributes')
	presets = fields.One2many('hassio.presets','entity_id',string="Presets")
	
	def get_data(self):
		# on va chercher dans les states la liste des entity
		for state in self.env['hassio.states'].search([]):
			domain = state.name.split('.')[0]
			sous_domain = state.name.split('.')[1]
			entity_id = self.search([('name','=',state.name)],limit=1)
			
			value = {
				'name': state.name,
				'friendly_name': json.loads(state.attributes)['friendly_name'],
				'ttype': self.env['hassio.entity_type'].search([('code','=',domain)]),
				'attributes': state.attributes
			}
			hassio_domain = self.env['hassio.services'].search([('name','=',domain)])
			value['services'] = [(6,0,hassio_domain.services.ids)]
			
			if not entity_id:
				self.create(value)
			else:
				entity_id.write(value)	
				
class hassio_events(models.Model):
	_name = 'hassio.events'
	
	name = fields.Char('Event')
	listener_count = fields.Integer('Listener Count')
	
	def get_data(self):
		url_base = self.env.user.company_id.hassio_server
		headers = {
			"Authorization": "Bearer {}".format(self.env.user.company_id.hassio_token),
			"content-type": "application/json",
		}
		
		url = "{}{}".format(url_base,"/api/events")
		logger.info(url)
		response = get(url, headers=headers)
		
		for event in json.loads(response.text):
			event_id = self.search([('name','=',event['event'])])
			
			value = {
				'name': event['event'],
				'listener_count': event['listener_count']
			}
			if not event_id:
				self.create(value)
			else:
				event_id.write(value)


	
class hassio_service(models.Model):
	_name = "hassio.service"

	name = fields.Char('Nom')
	
	
	def execute(self):
		logger.info(self.env.context)
		if self.env.context.get('entity_id',False):
			url_base = self.env.user.company_id.hassio_server
			headers = {
				"Authorization": "Bearer {}".format(self.env.user.company_id.hassio_token),
				"content-type": "application/json",
			}
			domain = self.env.context.get('entity_id').split('.')[0]
			url = "{}{}".format(url_base,"/api/services/{}/{}".format(domain,self.name))
			data = {
				"entity_id": self.env.context.get('entity_id'),
			}
			if self.env.context.get('service_data',False):
				data.update(json.loads(self.env.context.get('service_data')))
			
			logger.info(data)
			response = post(url, headers=headers,data=json.dumps(data))
	

class hassio_services(models.Model):
	_name = "hassio.services"

	name = fields.Char('Domain')
	services = fields.Many2many('hassio.service',string="Services")

	def get_data(self):
		url_base = self.env.user.company_id.hassio_server
		headers = {
			"Authorization": "Bearer {}".format(self.env.user.company_id.hassio_token),
			"content-type": "application/json",
		}
		
		url = "{}{}".format(url_base,"/api/services")
		logger.info(url)
		response = get(url, headers=headers)
		
		for service in json.loads(response.text):
			service_id = self.search([('name','=',service['domain'])])
			
			value = {
				'name': service['domain'],
			}
			services = []
			for s in service['services']:
				services.append((0,0,{'name': s}))
			value['services'] = services
			if not service_id:
				self.create(value)
			else:
				service_id.write(value)

class hassio_states(models.Model):
	_name = "hassio.states"

	name = fields.Char('Entity')
	attributes = fields.Text('Attributes')
	last_changed = fields.Datetime('Last changed')
	state = fields.Char('State')
	
	def get_data(self):
		url_base = self.env.user.company_id.hassio_server
		headers = {
			"Authorization": "Bearer {}".format(self.env.user.company_id.hassio_token),
			"content-type": "application/json",
		}
		
		url = "{}{}".format(url_base,"/api/states")
		logger.info(url)
		response = get(url, headers=headers)
		
		for state in json.loads(response.text):
			entity_id = self.search([('name','=',state['entity_id'])])
			
			value = {
				'name': state['entity_id'],
				'attributes': json.dumps(state['attributes']),
				'last_changed': datetime.strptime(state['last_changed'][0:19],"%Y-%m-%dT%H:%M:%S"),
				'state': state['state'],
			}
			if not entity_id:
				self.create(value)
			else:
				entity_id.write(value)
				