# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)
import requests

list_command = [ 'play', "pause", 'playpause', 'stop', 'next', 'previous' ]


class odoo_hifiberry(models.Model):
	_name = 'odoo.hifiberry'
	
	name = fields.Char('Nom')
	server = fields.Char('URL server')
	status = fields.Text('Status')
	log = fields.Text('Log')
	
	def get_player_status(self):
		if self.server:
			r = requests.get(self.server)
			self.status = r.text
			
	def player_command(self,command):
		if self.server and command in list_command:
			r = request.post("{}/api/player/{}".format(self.server,command)
			self.log = r.text