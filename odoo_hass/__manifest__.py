# -*- coding: utf-8 -*-

{
    "name": "Odoo HASS",
    "version": "1.0",
    "author": "François Le Gal",
    "website": "https://github.com/fanchlegal/odoobox",
    "license": "AGPL-3",
    "category": "Vertical",
    "description": "Odoo HASS - Connexion entre Odoo et HassIO",
    "depends": [
        'base',
    ],
    "data": [
        'security/ir.model.access.csv',
		'views/res_company.xml',
        'views/hassio.xml',
    ],
    "demo": [
	    
    ],
    'qweb': [
	    
    ],
    'installable': True,
	'application':True,
}
