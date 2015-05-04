# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'MA Payroll',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
MA Payroll
======================================

    * Salary

    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['hr', 'hr_ma', 'hr_grade', 'report_webkit'],
    'data': [
        'security/ir.model.access.csv',
        'hr_payroll_view.xml',
        'wizard/hr_salary_import_view.xml',
        'hr_payroll_ma_report.xml',
        'data/hr.salary.rule.csv',
        'data/hr.salary.residence.csv',
        'data/hr.salary.chapter.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
