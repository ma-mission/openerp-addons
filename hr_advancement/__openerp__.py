# -*- coding: utf-8 -*-
{
    'name': 'Employee advancement',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Employee advancement
============================

Employe advancement
    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['hr_evaluation_ma', 'report_webkit'],
    'data': [
        'hr_advancement_view.xml',
        'wizard/hr_advancement_compute_view.xml',
        'security/ir.model.access.csv',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
