# -*- coding: utf-8 -*-

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
