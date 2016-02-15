# -*- coding: utf-8 -*-

{
    'name': 'Patrimoine',
    'version': '2.0',
    'category': 'Patrimoine',
    'description': """
Outils:
=======
    * Gestion de patrimoine
    * Gestion de stock
    

    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['base','hr','l10n_ma_base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'menu.xml',
        'famille_view.xml',
        'sous_famille.xml',
        'categorie_view.xml',
        'article_view.xml',
        'reception.xml',
        'site_view.xml',
        'batiment_view.xml',
        'piece_view.xml',
        'sortie_view.xml',
        'patrimoine_reports.xml',
        'employe_view.xml',
        'receptionfourniture.xml',
        'sortiefourniture_view.xml',
        'fourniture_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
