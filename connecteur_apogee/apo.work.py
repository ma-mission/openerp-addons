#! /usr/bin/env python
# -*- coding:utf-8 -*-

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
from openerp import pooler
from openerp import tools
from tools.translate import _
from openerp.osv import osv,fields
import cx_Oracle
import os
import ast
import logging

_logger = logging.getLogger('Test openerp 2')

class apo(osv.osv):
    
    _name = 'apogee.filiere' 
    
    _description = 'Filieres' 

    os.environ['NLS_LANG'] = 'FRENCH_FRANCE.WE8ISO8859P9'

    def get_config(self, cr, uid):

        config = self.pool.get('apogee.config')
        ids = config.search(cr, uid, [])
        cfgs = config.browse(cr, uid, ids, [])

        return cfgs[0] if cfgs else None


    def load_data(self, cr, uid, context=None):
	
	cfg = self.get_config(cr, uid)

	model = 'apogee.etablissement'
	
        conn = cx_Oracle.connect(cfg.username, cfg.password, cfg.address+':1521/'+cfg.sid)
        cur = conn.cursor()
        stats = cur.execute('''
            SELECT COD_CMP, LIB_CMP, LIC_CMP FROM COMPOSANTE
            ''',)
	d = {}
	i = 1
	for stat in stats:
		d = {'code': stat[0],'name': stat[1], 'id': i}

		self.pool.get('apogee.etablissement').create(cr, uid, {'code': stat[0],'name': stat[0],})
		print stat
                _logger.info('APOGEE - Etablissement %s est %s:' % (stat[0],stat[1],))
		i = i+1
	
	return d

    def stats_cmp(cr, uid, stat):
	_logger.info('%s rules not found:' % (stat,))
        stats = self.ora_exec('''
            SELECT COD_CMP, COUNT(*) FROM INS_ADM_ETP WHERE COD_ANU=:anu AND ETA_IAE='E' GROUP BY COD_CMP
            ''', anu=2014)
	for stat in stats:
		print stat
		_logger.info('APOGEE - INS_ADM_ETP pour 2014 est de %s :' % (stat,))
        return stats
        #return list(stats)


#    if __name__ == '__main__':
#        stats = []
#        stats = stats_cmp(2014)
#        for stat in stats:
#            print(stat)

    
apo()
