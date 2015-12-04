
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenCourse(ses/.
#
##############################################################################
from openerp.osv import osv,fields

class apogee_effectif_inscrit(osv.osv):
    
    _name = 'apogee.effectif_inscrit'
    
    _description = 'Effectif des inscrits' 

    _columns = {
              'annee':fields.integer(string='Annee'),
              'nbr':fields.integer(string='Effectif des etudiants', size=256),
              'type':fields.selection((('reussi','Ayant Reussi'), ('nonreussi','Non Reussi')), string='Effectif des reussi'),
			  'filiere_id':fields.many2one('apogee.filiere', string='Filiere'),
			  'diplome_id':fields.related('filiere_id','diplome_id',type='many2one',relation='apogee.diplome', string='Diplome',store=True),
			  'etablissement_id':fields.related('filiere_id','diplome_id','etablissement_id',type='many2one',relation='apogee.etablissement', string='Etablissement',store=True),
                }
    
apogee_effectif_inscrit()