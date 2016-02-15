# -*- coding: utf-8 -*-

{
    'name': 'Employee Grade',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Add grade information on the employee.
======================================

    * Grade
    * Echelon
    * Indice

    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['hr'],
    'data': [
        'hr_grade_view.xml',
        'hr_employee_view.xml',
        'hr_paygrade_view.xml',
        'security/ir.model.access.csv',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
