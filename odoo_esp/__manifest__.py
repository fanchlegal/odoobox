# -*- coding: utf-8 -*-

{
    "name": "Odoo ESP",
    "version": "1.0",
    "author": "François Le Gal",
    "website": "https://github.com/fanchlegal/odoobox",
    "license": "AGPL-3",
    "category": "Vertical",
    "description": "Odoo ESP - Connexion entre Odoo et ESPHome",
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
