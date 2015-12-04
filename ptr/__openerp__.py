
{
    'name' : 'Patrimoine Tempus MISSION',
    'version' : '1.0',
    'author' : 'Equipe National ',
    'category' : 'TEMPUS MISSION',
	'sequence': '1',
    'description' : """
	
Module de gestion du patrimoin de l'USMS.
======================================================

Ce module couvre les éléments suivants:
------------------------------------------------------
    * Gestion des locaux
    * Gestion des équipements
    * Gestion des inventaires
    * Gestion des interventions de maintenance
   """,
    'website': 'http://www.tempusmission.ma',
    'images' : [''],
    'depends' : ['base','board', 'rh'],
    'data': [],
    'update_xml': ['ptr_etablissement_view.xml',
				   'ptr_patrimoinegeo_view.xml',
				   #'ptr_personnel_view.xml',
				   'ptr_patrimoineactif_view.xml',
				   'ptr_fournisseur_view.xml',
				   'ptr_inventaire_view.xml',
				   'ptr_detailinventaire_view.xml',
				   'ptr_intervention_view.xml',
				   'ptr_prestation_view.xml',
				   'ptr_reglement_view.xml',
				   'ptr_configuration_lists_view.xml',
				   'ptr_board_view.xml',
				   'ptr_inv_view.xml',
				   'ptr_inventaire_view.xml',
				   'workflow/ptr_inv_wkf.xml',
				   'workflow/ptr_inv_wkf1.xml',


				  ],
    'js': [],
    'qweb' : [],
    'css':[],
    'demo': [],
    'test': [],
	'application': True,
    'installable': True,
    'auto_install': False,
}
