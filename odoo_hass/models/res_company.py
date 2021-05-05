# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


class res_company(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'
	
	hassio_server = fields.Char('HassIO Serveur')
	hassio_token = fields.Char('Hassio Token')
	