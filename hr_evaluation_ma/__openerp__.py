# -*- coding: utf-8 -*-

{
    'name': 'MA Evaluation',
    'version': '1.0',
    'category': '',
    'description': """
Evaluation
======================================

    * item

    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['hr_ma', 'hr_grade'],
    'data': [
        'security/ir.model.access.csv',
        'hr_evaluation_view.xml',
        'hr_evaluation_report.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
