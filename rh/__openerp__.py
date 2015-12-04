{
    'name': 'RH Tempus MISSION',
    'version': '3.0',
    'author': 'SALHI Abderrahim',
    'category': 'Ressources Humaines',
    'sequence': '1',
    'summary': 'Tempus MISSION',
    'description': """
Human Ressources Management
==================================

Gestion des Ressources Humaines
    """,
    'website': 'http://www.uh1.ac.ma',
    'images': [    ],
    'depends': ['base','report_webkit','board', 'ptr_geo'],
    'data': [ 'rh_employe_view.xml',
			  'rh_ordre_mission_view.xml',
			  'rh_demande_view.xml',
			  'rh_fonction_view.xml',
			  'rh_salary_view.xml',
			  'rh_study_view.xml',
			  #'rh_etablissement_view.xml',
			  #'rh_departement_view.xml',
			  'rh_fonction_tables_view.xml',
			  'rh_autres_tables_view.xml',
			  'rh_reports.xml',
			  'workflows/rh_ordre_mission_wkf.xml',
			  'wizards/rh_reports_view.xml',
			  'wizards/rh_import_data_view.xml',
			  'wizards/rh_import_salary_view.xml',
			  #'rh_board_view.xml',
			  
				],
    'demo': [],
    'test': [
				],
    'installable': True,
    'active': False,
    'application': True,
    'auto_install': False,
    'css': ['static/css/rh.css'],
	'js': [
        	]
}
