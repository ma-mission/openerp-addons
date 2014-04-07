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
    'name': 'MA Employee',
    'version': '1.1',
    'author': 'Zakaria',
    'category': 'Human Resources',
    'sequence': 150,
    'summary': 'Ma Univ Employee',
    'description': """
Human Resources Management
==========================

HR Localization
    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'images': [
    ],
    'depends': ['hr', 'report_webkit'],
    'data': [
        'hr_report.xml',
        'hr_view.xml',
        'data/hr.job.csv',
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'active': False,
    'application': False,
    'auto_install': False,
    'css': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
