
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

class apogee_globalins(osv.osv):
    
    _name = 'apogee.globalins'
    
    _description = 'Effectif Global des inscrits' 

    def _get_total_globalins(self,cr,uid,ids,fields,args,context=None):
        
        result = 0
        
        for apogee_globalins in self.browse(cr,uid,ids,context) :
            result = result + apogee_globalins.nbr
        return result

    _columns = {
              	'nbr':fields.integer(string='Effectif des etudiants', size=256),
	      		'cod_cmp':fields.char(string='Etablissement', size=20),
	      		'lic_tpd':fields.char(string='Lib filiere', size=20),
	      		'lib_dip':fields.text(string='Lib diplome'),
	      		'province':fields.text(string='Province'),
	      		'pays':fields.text(string='Pays'),
	      		'univ':fields.text(string='Universite'),
              	'annee':fields.integer(string='Annee'),
		        #'total_count': fields.function(_get_total_globalins, type='integer', string='Effectif Global des Inscrits',store=True), 
                }
    
apogee_globalins()
