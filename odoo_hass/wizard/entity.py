# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class wizard_hassio_entity(models.TransientModel):
	_name = 'hassio.entity.wizard'
	
	color = fields.Integer('Couleur')
	
	def add_preset(self):
		self.name  = "test"
		return {}
