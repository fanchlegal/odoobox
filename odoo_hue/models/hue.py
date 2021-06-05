# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)
import phue

def rgb_to_xy(red, green, blue):
	""" conversion of RGB colors to CIE1931 XY colors
	Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
	Args: 
		red (float): a number between 0.0 and 1.0 representing red in the RGB space
		green (float): a number between 0.0 and 1.0 representing green in the RGB space
		blue (float): a number between 0.0 and 1.0 representing blue in the RGB space
	Returns:
		xy (list): x and y
	"""

	# gamma correction
	red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
	green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
	blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

	# convert rgb to xyz
	x = red * 0.649926 + green * 0.103455 + blue * 0.197109
	y = red * 0.234327 + green * 0.743075 + blue * 0.022598
	z = green * 0.053077 + blue * 1.035763

	# convert xyz to xy
	x = x / (x + y + z)
	y = y / (x + y + z)

	# TODO check color gamut if known
	 
	return [x, y]

class hue_group(models.Model):
	_name = "hue.group"

	name = fields.Char('Name')
	bridge_id = fields.Many2one('hue.bridge',string="Bridge")
	lights = fields.One2many('hue.light','group_id',string='Lights')
	
class hue_schedule(models.Model):
	_name = "hue.schedule"

	name = fields.Char('Name')
	bridge_id = fields.Many2one('hue.bridge',string="Bridge")

class hue_light(models.Model):
	_name = 'hue.light'
	
	name = fields.Char('Name')
	brightness = fields.Integer('Brightness')
	on = fields.Boolean('On')
	hue = fields.Integer('Hue')
	saturation = fields.Integer('Saturation')
	light_id = fields.Integer('Light ID')
	bridge_id = fields.Many2one('hue.bridge',string="Bridge")
	group_id = fields.Many2one('hue.group',string="Group")
	
	@api.onchange('on')
	def onchange_on(self):
		b = phue.Bridge(self.bridge_id.server)
		lights = b.get_light_objects('id')
		light = lights[self.light_id]
		light.on = self.on
			
			
	@api.onchange('brightness','hue','saturation')
	def onchange_brightness(self):
		b = phue.Bridge(self.bridge_id.server)
		lights = b.get_light_objects('id')
		light = lights[self.light_id]
		if self.brightness:
			light.brightmess = self.brightness
		"""
		if self.hue:
			b.set_light(light_id,'hue',self.hue)
		if self.saturation:
			b.set_light(light_id,'saturation',self.saturation)
		"""
	
	def set_on(self):
		b = phue.Bridge(self.bridge_id.server)
		lights = b.get_light_objects('id')
		for l in self:
			light = lights[l.light_id]
			light.on = True
	
	def set_off(self):
		b = phue.Bridge(self.bridge_id.server)
		lights = b.get_light_objects('id')
		for l in self:
			light = lights[l.light_id]
			light.on = False		
			
class hue_bridge(models.Model):
	_name = 'hue.bridge'
	
	name = fields.Char('Name')
	server = fields.Char('Server')
	registered = fields.Boolean('Registered')
	lights = fields.One2many('hue.light','bridge_id',string='Lights')
	groups = fields.One2many('hue.group','bridge_id',string='Groups')
	schedules = fields.One2many('hue.schedule','bridge_id',string="Schedules")
	
	def register(self):
		b = phue.Bridge(self.server)
		b.connect()
		self.registered = True
		
	def update(self):
		b = phue.Bridge(self.server)
		
		# get Lights
		lights = b.lights
		
		for light in lights:
			logger.info(light.__dict__)
			value = {
				'name': light.name,
				'light_id': light.light_id,
				'on': light.on,
				'brightness': light.brightness,
				#'saturation': light.saturation,
				#'hue': light.hue,
				'bridge_id': self.id
			}
			odoo_light = self.env['hue.light'].search([('light_id','=',light.light_id)])
			if odoo_light:
				odoo_light.write(value)
			else:
				self.env['hue.light'].create(value)
				
		groups = b.get_group()
		logger.info(groups)
		for group in groups.keys():

			value = {
				'name': groups[group]['name'],
				'bridge_id': self.id	
			}
			odoo_group = self.env['hue.group'].search([('name','=',group)])
			if odoo_group:
				odoo_group.write(value)
			else:
				ooo_group = self.env['hue.group'].create(value)
			
			for light_id in groups[group]['lights']:
				light = self.env['hue.light'].search([('light_id','=',int(light_id))])
				light.group_id = odoo_group.id
			
		schedules = b.get_schedule()
		for schedule in schedules:
			value = {
				'name': schedule,
				'bridge_id': self.id
			}
			odoo_schedule = self.env['hue.schedule'].search([('name','=',schedule)])
			if odoo_schedule:
				odoo_schedule.write(value)
			else:
				self.env['hue.schedule'].create(value)