# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


class res_company(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'
	
	min_probability = fields.Float('Probabilité minimum de reconnaissance',default=0.8)