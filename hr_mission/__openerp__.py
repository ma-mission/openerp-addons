# -*- coding: utf-8 -*-

{
    'name': 'Mission',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Missions
========

    * Ordres de missions

    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['hr', 'l10n_ma_base', 'report_webkit'],
    'data': [
        'security/ir.model.access.csv',
        'hr_mission_view.xml',
        'hr_mission_workflow.xml',
        'hr_mission_report.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
