# -*- coding: utf-8 -*-

{
    'name': 'Budget',
    'version': '1',
    'category': 'Accounting',
    'summary': 'MA Univ Budget Accounting',
    'description': """
Moroccan Budget Accounting
==========================

Budget Accounting for moroccan universities.
    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['account'],
    'data': [
        'budget_view.xml',
        'commitment_view.xml',
        'menu_hide.xml',
        'data/account.analytic.journal.csv',
        'data/account.analytic.account.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
