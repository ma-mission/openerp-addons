# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2014 Université Hassan 1er.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'RH MA',
    'version': '1.2',
    'author': 'SALHI Abderrahim',
    'category': 'Ressources Humaines',
    'sequence': 1,
    'summary': 'MA RH University',
    'description': """
Human Ressources Management
==================================

Gestion des Ressources Humaines
    """,
    'website': 'http://www.USMS.MA',
    'images': [    ],
    'depends': ['base','board','report_webkit'],
    'data': [
        'rh_view.xml',
        'rh_establishment_view.xml',
		'rh_department_view.xml',
		'rh_job_view.xml',
		'rh_study_view.xml',
		'rh_reports.xml',
		'wizards/reports_view.xml',
		'rh_request_view.xml',
		'rh_board_view.xml',
		'rh_mailer_view.xml',
		'rh_partner_view.xml',
		'rh_stady_wkf.xml',
		
				],
    'demo': [],
    'test': [
				],
    'installable': True,
    'active': False,
    'application': False,
    'auto_install': False,
    'css': ['static/css/rh.css',],
	'js': [
        #'static/js/rh.js',
		]
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
