# -*- coding: utf-8 -*-

import json

from odoo import exceptions, _, http
from odoo.http import Controller, request, route


class HomeBusController(Controller):
	
	
	@http.route('/bus/post', type='http', auth="public",csrf=False)
	def bus_post(self,login,password,channel,type,message):
		logger.info(request.params)
		try:
			uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
			
			request.env['bus.bus']._sendone(request.params['channel'],request.params['type'],request.params['message'])
			logger.info("Message MQTT reçu")
			
			
			
		except odoo.exceptions.AccessDenied as e:
			logger.info(str(e))
			return request.not_found()
			
		return True