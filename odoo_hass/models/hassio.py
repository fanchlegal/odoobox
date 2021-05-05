# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


class hassio_events(models.Model):
	_name = 'hassio.events'
	
	name = fields.Char('Event')
	listener_count = fields.Integer('Listener Count')
	

class hassio_service(models.Model):
	_name = "hassio.service"

	name = fields.Char('Nom')

class hassio_services(models.Model):
	_name = "hassio.services"

	name = fields.Char('Domain')
	services = fields.Many2many('hassio.service',string="Service")

class hassio_states(models.Model):
	_name = "hassio.states"

	name = fields.Char('Entity')
	attributes = fields.Text('Attributes')
	last_changed = fields.Datetime('Last changed')
	state = fields.Char('State')
	