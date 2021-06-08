# -*- coding: utf-8 -*-

{
    "name": "Odoo HifiBerry",
    "version": "1.0",
    "author": "François Le Gal",
    "website": "https://github.com/fanchlegal/odoobox",
    "license": "AGPL-3",
    "category": "Vertical",
    "description": "Odoo HifiBerry - Connexion entre Odoo et HifiBerryOS",
    "depends": [
        'base',
    ],
    "data": [
        'security/ir.model.access.csv',
		'views/res_company.xml',
        'views/hifiberry.xml'
    ],
    "demo": [
	    
    ],
    'qweb': [
	    
    ],
    'installable': True,
	'application':True,
}
