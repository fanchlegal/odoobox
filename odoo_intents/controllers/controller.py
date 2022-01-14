# -*- coding: utf-8 -*-


from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.fields import Command
from odoo.http import request

class website_odoo_intents(http.Controller):
	
	@http.route(['/intents/'], type='http', auth="public", website=True)
	def intents(self,**kwargs):
		
		intent = request.params.get('intent')
		
		logger.info('Intention : {}'.format(intent))
		
		nlu = {
			"intent": {
				"intentName": "searchWeatherForecast",
				"probability": 0.95
			},
		    "slots": [
			    {
				"value": "paris",
				"entity": "locality",
				"slotName": "forecast_locality"
			},
			{
				"value": {
					"kind": "InstantTime",
					"value": "2018-02-08 20:00:00 +00:00"
				},
				"entity": "snips/datetime",
				"slotName": "forecast_start_datetime"
			}
		   ]
		}
		
		odoo_intent = self.env['odoo.intent'].search([('name','=',intent)])
		
		if odoo_intent:
		
			odoo_intent.run()
		
		else:
			# on demande à NLU de nous donner l'intention
			nlu_intent = nlu.get('intent')
			if nlu_intent['probability'] > self.env.user.company_id.min_probability:
				odoo_intent = self.env['odoo.intent'].search([('name','=',nlu_intent['intentName'])])
				if odoo_intent:
					odoo_intent.run(nlu_intent['slots'])
				else:
					value_intent = {
						'name': nlu_intent['intentName'],
						'slots': nlu_intent['slots'],
						'connue': False,
					}
					self.env['odoo.intent'].create(value_intent)
			else:
				logger.info("Probabilité trop basse, pas d'exécution")
					
					
					
		return {}