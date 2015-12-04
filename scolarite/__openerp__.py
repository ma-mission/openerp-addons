# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Scolarité Tempus MISSION",
    "version": "1.0",
    "depends": ["base","report_webkit","board"],
    "author": "SABRI Mouhcine",
    "category": "SCOLARITE",
    "description": """
        Apogee module for managing Report:
            - Taux des Scollicitations des filieres
            - Etablissements
            - Diplomes
            - Filieres
            - Effectif des Inscrits Par Filiére 
    """,
    "sequence": "1",
    "init_xml": [],
    'js': ['static/src/js/load.js'],
    'update_xml': ['sollicitationfiliere_view.xml','tauxreussite_view.xml','effectif_globalins_view.xml','effectif_newins_view.xml'],
    'data':['security/apogee.etablissement.csv',
			'security/apogee.diplome.csv',
			'security/apogee.filiere.csv',
			'security/apogee.effectif_inscrit.csv',
			'security/apogee.globalins.csv'
			],
    'installable': True,
	'application': True,
    'active': False,
}
