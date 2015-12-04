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
    'name': 'Finance',
    'version': '1.0',
    'category': '',
    'description': """
Outils:
=======
    * Repartition des budgets par rubrique
    * Engagements
    * Gestion de documents (OP/Contrat...)

    """,
    'author': 'UH1',
    'website': 'http://www.uh1.ac.ma',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'menu.xml',
        'gestion_budget_view.xml',
        'compte_view.xml',
        'axe_view.xml',
        'credit.xml',
        'article_view.xml',
        'nature_view.xml',
        'appelof_view.xml',
        'appelof_workflow.xml',
        'fournisseur_view.xml',
        'devis_view.xml',
        'budget_workflow.xml',
        'engagement_view.xml',
        'engagement_report.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
