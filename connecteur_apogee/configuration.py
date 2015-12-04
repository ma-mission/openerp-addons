
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

class Configuration(osv.osv):
    
    _name = 'apogee.config' 
    
    _description = 'Configuration of APOGEE' 

    def create(self, cr, uid, default, context=None):
        res = super(Configuration, self).create(cr, uid, default, context=context)
        if len(self.search(cr, uid, [])) > 1:
            raise osv.except_osv('Attention','Vous avez droit a un seul enregistrement APOGEE')
        return res
    
    _columns = {
              'address':fields.char('Adresse du serveur APOGEE', size=64, required=True, readonly=False),
              'sid':fields.char('SID de la base de données APOGEE', size=64, required=True, readonly=False), 
              'username':fields.char('Utilisateur APOGEE', size=120, required=True, readonly=False), 
              'password':fields.char('Mot de Passe', size=200, required=True, readonly=False),
              'nls_lang':fields.char('Jeu de caractéres', size=200, required=True, readonly=True),
                }

    _defaults = {
        'address': '10.0.0.10',
        'sid': 'APOGEEPROD',
        'username': 'Mot de passe utilisateur APOGEE',
	'password': 'Mot de passe',
	'nls_lang': 'FRENCH_FRANCE.WE8ISO8859P9',
        }

    
Configuration()
