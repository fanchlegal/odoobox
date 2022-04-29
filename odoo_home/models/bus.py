# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


class bus_bus(models.Model):
	_name = 'bus.bus'
	_inherit = 'bus.bus'
	
	@api.model
	def sendone(self, channel, notification_type, message):
		self._sendmany([[channel, notification_type, message]])