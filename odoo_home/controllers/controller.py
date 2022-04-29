# -*- coding: utf-8 -*-

import json

from odoo import exceptions, _
from odoo.http import Controller, request, route


class HomeBusController(Controller):
	
	
	@http.route('/lonpolling/post', type='http', auth="public")
	def longpolling_post(self,login,password,channel,type,message):
		try:
			uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
			
			request.env['bus.bus']._sendone(request.params['channel'],request.params['type'],request.params['message'])
			
			
			
			
		except odoo.exceptions.AccessDenied as e:
			logger.info(str(e))
			return request.not_found()
			
		return True