# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class odoo_action(models.Model):
	_name = 'odoo.action'
	
	name = fields.Char('Nom')
	action = fields.Text('Action')

	def run(self):
		
		logger.info("run action {}".format(self.name))
		logger.info("action : {}".format(self.action))
		
		
class odoo_intent(models.Model):
	_name = 'odoo.intent'
	
	name = fields.Char('Nom')
	slots = fields.Text('Slots')
	actions = fields.Many2many('odoo.action',string="Actions")
	connue = fields.Boolean('Intention connue')
	
	
	def run(self,slots=False):
		logger.info("run intent {}".format(self.name))
		if not slots:
			slots = self.slots
			
		logger.info("slots : {}".format(slots))