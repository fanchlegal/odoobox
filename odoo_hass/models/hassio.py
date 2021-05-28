# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)
from requests import get,post
import json
from datetime import datetime

class hassio_entity(models.Model):
	_name = "hassio.entity"
	
	name = fields.Char('Entity')
	services = fields.Many2many('hassio.service',string="Services")
	
	def get_data(self):
		# on va chercher dans les states la liste des entity
		for state in self.env['hassio.states'].search([]):
			domain = state.name.split('.')[0]
			sous_domain = state.name.split('.')[1]
			entity_id = self.search([('name','=',state.name)],limit=1)
			if not entity_id:
				value = {
					'name': state.name,
				}
				hassio_domain = self.env['hassio.services'].search([('name','=',domain)])
				value['services'] = [(6,0,hassio_domain.services.ids)]
				self.create(value)
			else:
				hassio_domain = self.env['hassio.services'].search([('name','=',domain)])
				entity_id.services = (6,0,hassio_domain.services.ids)
				
				
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
			if not self.search([('name','=',event['event'])]):
				value = {
					'name': event['event'],
					'listener_count': event['listener_count']
				}
				self.create(value)
		
	
class hassio_service(models.Model):
	_name = "hassio.service"

	name = fields.Char('Nom')
	
	def execute(self):
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
			response = post(url, headers=headers,data=json.dumps(data))
			logger.info(response.text)
	

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
			if not self.search([('name','=',service['domain'])]):
				value = {
					'name': service['domain'],
				}
				services = []
				for s in service['services']:
					services.append((0,0,{'name': s}))
				value['services'] = services
					
				self.create(value)

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
			if not self.search([('name','=',state['entity_id'])]):
				value = {
					'name': state['entity_id'],
					'attributes': state['attributes'],
					'last_changed': datetime.strptime(state['last_changed'][0:19],"%Y-%m-%dT%H:%M:%S"),
					'state': state['state'],
				}
				self.create(value)
				