# -*- coding: utf-8 -*-

{
    "name": "Odoo Intents",
    "version": "1.0",
    "author": "François Le Gal",
    "website": "https://github.com/fanchlegal/odoobox",
    "license": "AGPL-3",
    "category": "Vertical",
    "description": "Odoo Intents - Intentions dans odoo box",
    "depends": [
        'base',
    ],
    "data": [
        'security/ir.model.access.csv',
		'views/res_company.xml',
        'views/odoo_intent.xml',
    ],
    "demo": [
	    
    ],
    'qweb': [
	    
    ],
    'installable': True,
	'application':True,
}
