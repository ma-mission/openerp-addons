# -*- coding: utf-8 -*-

{
    'name': 'Employee Studies',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Employee Studies
================

Track employees' studies

    """,
    'author': 'Mission',
    'depends': ['hr'],
    'data': [
        'hr_study_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

