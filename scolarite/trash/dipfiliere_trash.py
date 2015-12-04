
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp.osv import osv,fields

class Dipfiliere(osv.osv):
    
    _name = "inscrits.dipfiliere"

    _columns = {
        'cod_etab' : fields.char(string="Code Etab", size=256),
        'lib_etab': fields.text('libelle etablissement'),
        'cod_dip' : fields.char(string="Code diplome", size=256),
        'lib_dip': fields.text('libelle diplome'),
        'cod_filiere' : fields.char(string="Code filiere", size=256),
        'lib_filiere': fields.text('libelle filiere'),
        'annee': fields.integer('Annee'),
        'type':fields.char('Global ou Nouveaux inscrits', size=64, required=True),
        'nbr': fields.integer('Effectif des Inscrits'),
    }
Dipfiliere()