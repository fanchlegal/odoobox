# -*- coding: utf-8 -*-

{
    "name": "Odoo Hue",
    "version": "1.0",
    "author": "François Le Gal",
    "website": "https://github.com/fanchlegal/odoobox",
    "license": "AGPL-3",
    "category": "Vertical",
    "description": "Odoo HUE - Connexion entre Odoo et Hue",
    "depends": [
        'base',
    ],
    "data": [
        'security/ir.model.access.csv',
		'views/res_company.xml',
    ],
    "demo": [
	    
    ],
    'qweb': [
	    
    ],
    'installable': True,
	'application':True,
}
