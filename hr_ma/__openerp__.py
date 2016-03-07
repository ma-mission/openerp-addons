# -*- coding: utf-8 -*-

{
    'name': 'MA Employee',
    'version': '1.1',
    'category': 'Human Resources',
    'summary': 'Ma Univ Employee',
    'description': """
Human Resources Management
==========================

HR Localization
    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['hr', 'hr_grade', 'report_webkit'],
    'data': [
        'hr_report.xml',
        'hr_view.xml',
        'data/hr.job.csv',
        'data/hr.grade.category.csv',
        'data/hr.grade.csv',
        'report/card.xml',
        'res_config_view.xml',
    ],
    'css': ['static/src/css/style.css'],
    'demo': [
        'demo/hr.employee.csv',
        'demo/hr_demo.xml',
        'demo/hr.employee.grade.csv',
        ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
