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
from openerp.tools.translate import _
from openerp.osv import osv,fields
import cx_Oracle
import os
import ast
import logging

_logger = logging.getLogger('Log Module Connecteur')

class apo(osv.osv):
    
    _name = 'apogee.synchronization' 
    
    _description = 'Synchronization of data from apogee to openerp' 

    os.environ['NLS_LANG'] = 'FRENCH_FRANCE.WE8ISO8859P9'

    def init(self, cr):
	
        cron_ids = self.pool.get('ir.cron').search(cr, '1', [('model', '=', 'apogee.synchronization')], None)
	#self.pool.get('ir.cron').unlink(cr, '1', cron_ids)

	#cron_id = self.pool.get('ir.cron').create(cr, '1', {'function': 'load_data','name': 'toto', 'interval_type': 
	#						    'minutes', 'active': 'TRUE', 'interval_number': '1', 
	#						    'user_id': '1', 'numbercall': '-1', 'model': 
	#						    'apogee.synchronization'})


	#_logger.info('How can i execute a SQL statement on module update and installation?')
	
	return False

    def get_config(self, cr, uid):

        config = self.pool.get('apogee.config')
        ids = config.search(cr, uid, [])
        cfgs = config.browse(cr, uid, ids, [])

        return cfgs[0] if cfgs else None


    def sync_newins(self, cr, uid, context=None):

        cfg = self.get_config(cr, uid)

        id_globalins = self.pool.get('apogee.newins').search(cr, uid, [])
        self.pool.get('apogee.newins').unlink(cr, uid, id_globalins, context)

        conn = cx_Oracle.connect(cfg.username, cfg.password, cfg.address+':1521/'+cfg.sid)

        cur_global = conn.cursor()

        vals = cur_global.execute('''
		SELECT count(DISTINCT ins.cod_ind) nbr , ins.cod_cmp ,typ.lic_tpd , dip.LIB_DIP, 
			d.lib_dep as province, pays.lib_pay AS pays ,'UNIV',ins.cod_anu as annee
		FROM ins_adm_etp ins,  typ_diplome typ, diplome dip ,ind_bac b, individu i , Adresse ad ,pays, departement d
		WHERE ins.cod_anu     = (select max(cod_anu) from ANNEE_UNI ) AND ins.eta_iae     = 'E'  
		AND dip.cod_tpd_etb = typ.cod_tpd_etb 
		AND ins.cod_dip = dip.cod_dip 
		AND ins.cod_ind = i.cod_ind
		AND i.cod_ind = b.cod_ind
		AND d.cod_dep = b.cod_dep
		AND ins.cod_ind = ad.cod_ind 
		AND i.cod_ind = ad.cod_ind 
		AND i.cod_pay_nat = pays.cod_pay
		AND ins.nbr_ins_cyc = 1  
		AND ins.nbr_ins_dip = 1 
		AND ins.nbr_ins_etp = 1

		GROUP BY ins.cod_cmp ,typ.lic_tpd , dip.LIB_DIP, d.lib_dep , pays.lib_pay,ins.cod_anu
            ''',)

        ##################################
        #           Global Ins           #
        ##################################

        filter_str = """<?xml version="1.0"?> <search string="Search"> <field name="lib_dip" string="Code 
                        Etab"/> <separator/> <field name="annee" string="Annee"/> <group expand="1" 
                        string="Filtres">"""

        val_id = 1      

        for val in vals:

                val_id = self.pool.get('apogee.newins').create(cr, uid, {'nbr': val[0],'cod_cmp': 
                         val[1].replace("'"," ").decode('latin1'),'lic_tpd': val[2].replace("'"," ").decode('latin1'),
                         'lib_dip': val[3].replace("'"," ").decode('latin1'),'province': 
                         val[4].replace("'"," ").decode('latin1'),'pays': val[5].replace("'"," ").decode('latin1'),
                         'univ': val[6],'annee': val[7],})

                filter_etab = """<filter string="%s" icon="terp-personnal+" domain="[('COD_CMP','=',%s)]" />"""  % (val[1], val[1], )

                filter_str += filter_etab

        filter_str += """<separator/>
                         <filter string="2013-2014" icon="terp-personnal+" domain="[('annee','=',2013)]" />
                         <filter string="2014-2015" icon="terp-personnal+" domain="[('annee','=',2014)]" />
                         </group>
                         </search>"""

        views_ids = self.pool.get('ir.ui.view').search(cr, uid, [('model', '=', 'apogee.newins'), ('type', '=', 'search'), ('name', '=', 'newins.search')], context = context)


        views = self.pool.get('ir.ui.view').browse(cr, uid, views_ids, context = context)

        view = views[0]

        w = self.pool.get('ir.ui.view').write(cr, uid, views_ids, {'arch': filter_str.decode('latin1')}, context = context)


        _logger.info('Synchronization New Ins OK %s' % (val_id,))

        return val_id


    def sync_globalins(self, cr, uid, context=None):

	cfg = self.get_config(cr, uid)

        id_globalins = self.pool.get('apogee.globalins').search(cr, uid, [])
        self.pool.get('apogee.globalins').unlink(cr, uid, id_globalins, context)

        conn = cx_Oracle.connect(cfg.username, cfg.password, cfg.address+':1521/'+cfg.sid)

        cur_global = conn.cursor()

        vals = cur_global.execute('''
		SELECT count(DISTINCT ins.cod_ind) nbr , ins.cod_cmp ,typ.lic_tpd , dip.LIB_DIP, d.lib_dep as 
		 	province, pays.lib_pay AS pays ,'UNIV',ins.cod_anu as annee
		FROM ins_adm_etp ins,  typ_diplome typ, diplome dip ,ind_bac b, individu i , Adresse ad ,pays, departement d
		WHERE ins.cod_anu     = (select max(cod_anu) from ANNEE_UNI ) AND ins.eta_iae     = 'E'  
		AND dip.cod_tpd_etb = typ.cod_tpd_etb 
		AND ins.cod_dip = dip.cod_dip 
		AND ins.cod_ind = i.cod_ind
		AND i.cod_ind = b.cod_ind
		AND d.cod_dep = b.cod_dep
		AND ins.cod_ind = ad.cod_ind 
		AND i.cod_ind = ad.cod_ind 
		AND i.cod_pay_nat = pays.cod_pay

		GROUP BY ins.cod_cmp ,typ.lic_tpd , dip.LIB_DIP, d.lib_dep , pays.lib_pay,ins.cod_anu
            ''',)


        ##################################
        #           Global Ins           #
        ##################################

        filter_str = """<?xml version="1.0"?> <search string="Search"> <field name="lib_dip" string="Code 
                        Etab"/> <separator/> <field name="annee" string="Annee"/> <group expand="1" 
                        string="Filtres">"""

	val_id = 1	

        for val in vals:

                val_id = self.pool.get('apogee.globalins').create(cr, uid, {'nbr': val[0],'cod_cmp': 
			 val[1].replace("'"," ").decode('latin1'),'lic_tpd': val[2].replace("'"," ").decode('latin1'),
			 'lib_dip': val[3].replace("'"," ").decode('latin1'),'province': 
			 val[4].replace("'"," ").decode('latin1'),'pays': val[5].replace("'"," ").decode('latin1'),
			 'univ': val[6],'annee': val[7],})

                filter_etab = """<filter string="%s" icon="terp-personnal+" domain="[('COD_CMP','=',%s)]" />"""  % (val[1], val[1], )

                filter_str += filter_etab

        filter_str += """<separator/>
                         <filter string="2013-2014" icon="terp-personnal+" domain="[('annee','=',2013)]" />
                         <filter string="2014-2015" icon="terp-personnal+" domain="[('annee','=',2014)]" />
                         </group>
                         </search>"""

        views_ids = self.pool.get('ir.ui.view').search(cr, uid, [('model', '=', 'apogee.globalins'), ('type', '=', 'search'), ('name', '=', 'globalins.search')], context = context)

        views = self.pool.get('ir.ui.view').browse(cr, uid, views_ids, context = context)

        view = views[0]

        w = self.pool.get('ir.ui.view').write(cr, uid, views_ids, {'arch': filter_str.decode('latin1')}, context = context)


        _logger.info('Synchronization Global Ins OK %s' % (val_id,))

	return id_globalins

    def sync_etab_dip_fil(self, cr, uid, context=None):
	
	cfg = self.get_config(cr, uid)
	
	#cr.execute('ALTER SEQUENCE apogee_etablissement_id_seq RESTART WITH 1')
	#cr.execute('ALTER SEQUENCE apogee_diplome_id_seq RESTART WITH 1')
	#cr.execute('ALTER SEQUENCE apogee_filiere_id_seq RESTART WITH 1')
	#cr.execute('ALTER SEQUENCE apogee_effectif_inscrit_id_seq RESTART WITH 1')

	model = 'apogee.etablissement'

        id_etabs = self.pool.get('apogee.etablissement').search(cr, uid, [])
        self.pool.get('apogee.etablissement').unlink(cr, uid, id_etabs, context)

        old_dips = self.pool.get('apogee.diplome')
        ids = old_dips.search(cr, uid, [])
        self.pool.get('apogee.diplome').unlink(cr, uid, ids, context)

        old_fils = self.pool.get('apogee.filiere')
        ids = old_fils.search(cr, uid, [])
        self.pool.get('apogee.filiere').unlink(cr, uid, ids, context)

        old_effectifs = self.pool.get('apogee.effectif_inscrit')
        ids = old_effectifs.search(cr, uid, [])
        self.pool.get('apogee.effectif_inscrit').unlink(cr, uid, ids, context)
	
        conn = cx_Oracle.connect(cfg.username, cfg.password, cfg.address+':1521/'+cfg.sid)

        cur_etab = conn.cursor()
	cur_dip = conn.cursor()
	cur_fil = conn.cursor()
	cur_effectif = conn.cursor()

        etabs = cur_etab.execute('''
            SELECT COD_CMP, LIB_CMP, LIC_CMP FROM COMPOSANTE
            ''',)

	etab_id = 1
	dip_id = 1
	fil_id = 1
	effectif_id = 1

	filter_str = """<?xml version="1.0"?> <search string="Search"> <field name="etablissement_id" string="Code 
			Etab"/> <separator/> <field name="annee" string="Annee"/> <group string="Regrouper par :"> 
			<filter string="Etablissement" context="{'group_by':'etablissement_id'}"/> <filter 
			string="Diplome" context="{'group_by':'diplome_id'}"/> </group> <group expand="1" 
			string="Filtres">"""

	##################################
	#	  Etablissement		 #
	##################################

	for etab in etabs:

		etab_id = self.pool.get('apogee.etablissement').create(cr, uid, {'code': etab[0],'name': etab[1].replace("'", 
		" ").decode('latin1'),})

		filter_etab = """<filter string="%s" icon="terp-personnal+" domain="[('etablissement_id','=',%s)]" />""" % (etab[2], etab_id, )

		filter_str += filter_etab
		
		dips = cur_dip.execute('''SELECT distinct tp.cod_tpd_etb,tp.lic_tpd, tp.LIB_TPD, ins.COD_CMP
					FROM TYP_DIPLOME tp, DIPLOME dp , INS_ADM_ETP ins
					where tp.cod_tpd_etb = dp.COD_TPD_ETB and dp.COD_DIP = ins.COD_DIP
					and ins.COD_ANU = (select max(cod_anu) from ANNEE_UNI)
					AND ins.ETA_IAE  = 'E' AND ins.COD_CMP = '%s' ''' % (etab[0],) ,)

	        ################################## 
        	#              Diplome           #
	        ##################################  
		
		for dip in dips:

			dip_id = self.pool.get('apogee.diplome').create(cr, uid, {'code': dip[1],'name': dip[2].replace("'", " ").decode('latin1'),'etablissement_id': etab_id,})


	                fils = cur_fil.execute('''SELECT DISTINCT d.cod_dip, d.lic_dip, d.LIB_DIP, d.cod_tpd_etb 
						FROM DIPLOME d, INS_ADM_ETP ins
						where ins.COD_ANU = 2014
						AND ins.ETA_IAE = 'E' AND ins.COD_CMP = '%s' AND d.COD_DIP = ins.COD_DIP
                	                        AND d.COD_TPD_ETB = '%s' ''' % (dip[3],dip[0]) ,)

			fils_empty = []

		        ################################## 
		        #            Filiere             #
		        ##################################  
			
	                for fil in fils:
		             #fil_id = self.pool.get('apogee.filiere').create(cr, uid, {'code': fil[0],'name': 
		             #fil[2].replace("'", " ").decode('latin1'),}) 
			     fil_id = self.pool.get('apogee.filiere').create(cr, uid, {'diplome_id': dip_id,'code': fil[0],'name':
		             fil[2].replace("'", " ").decode('latin1'),})

                             #####################################
                             #        Effectif des inscrits      #
                             #####################################

			     reussi = 0
			     non_reussi = 0

	                     effectif = cur_effectif.execute('''SELECT inscr.nbrins,vld.nbr nbrlaureat,inscr.COD_CMP,inscr.lic_tpd,
								inscr.LIB_DIP, vld.cod_dip from (SELECT count(distinct 
								ins.cod_ind) nbr , ins.COD_CMP,dip.LIB_DIP ,vdi.cod_tre 
								,ins.cod_dip from INS_ADM_ETP ins , RESULTAT_VDI vdi, diplome 
								dip where ins.COD_IND = vdi.cod_ind AND vdi.cod_tre in('V') 
								and vdi.ETA_MND_VDI = 'C' AND ins.ETA_IAE = 'E' AND 
								ins.cod_dip = dip.cod_dip and dip.cod_dip = '%s' and 
								ins.cod_ind = vdi.cod_ind AND ins.COD_ANU = 2014 and 
								vdi.COD_ANU = 2014 group by ins.COD_CMP,dip.LIB_DIP , 
								vdi.cod_tre, ins.cod_dip) vld , ( SELECT count(distinct 
								INS_ADM_ETP.cod_ind) nbrins , 
								INS_ADM_ETP.COD_CMP,typ_diplome.lic_tpd,diplome.LIB_DIP from 
								INS_ADM_ETP , typ_diplome , diplome where diplome.cod_tpd_etb 
								= typ_diplome.cod_tpd_etb AND INS_ADM_ETP.cod_dip = 
								diplome.cod_dip and diplome.cod_dip = '%s' AND 
								INS_ADM_ETP.COD_ANU = 2014 AND INS_ADM_ETP.ETA_IAE = 'E' AND 
								INS_ADM_ETP.cod_ind in (select distinct cod_ind from 
								RESULTAT_VDI where COD_ANU = 2014) group by 
								INS_ADM_ETP.COD_CMP,typ_diplome.lic_tpd,diplome.LIB_DIP) inscr
								where vld.COD_CMP = inscr.COD_CMP and vld.LIB_DIP = 
								inscr.LIB_DIP ''' % (fil[0], fil[0]) ,).fetchone()

			     if effectif > 0:
			     	reussi = effectif[1]
			     	non_reussi = effectif[0] - reussi

			     	effectif_id = self.pool.get('apogee.effectif_inscrit').create(cr, uid, {'type': 'reussi','nbr': 
							reussi,'annee': '2014','filiere_id': 
							fil_id,'diplome_id':dip_id,'etablissement_id':etab_id,})

			     	effectif_id = self.pool.get('apogee.effectif_inscrit').create(cr, uid, {'type': 'nonreussi','nbr': 
							non_reussi,'annee': '2014','filiere_id': 
							fil_id,'diplome_id':dip_id,'etablissement_id':etab_id,})
			     else:
				fils_empty.append(fil_id)
			
			self.pool.get('apogee.filiere').unlink(cr, uid, fils_empty, context)

                             #for fil in fils:

	filter_str += """<separator/>
			 <filter string="2013-2014" icon="terp-personnal+" domain="[('annee','=',2013)]" />
			 <filter string="2014-2015" icon="terp-personnal+" domain="[('annee','=',2014)]" />
			 </group>
			 </search>"""
		
        views_ids = self.pool.get('ir.ui.view').search(cr, uid, [('model', '=', 'apogee.effectif_inscrit'), ('type', '=', 'search'), ('name', '=', 'effectif_inscrit.search')], context = context)

	views = self.pool.get('ir.ui.view').browse(cr, uid, views_ids, context = context)

	view = views[0]

	w = self.pool.get('ir.ui.view').write(cr, uid, views_ids, {'arch': filter_str.decode('latin1')}, context = context)


#	view.write(cr, uid, views_ids, vals, context=context)
#		print view.arch
	_logger.info('Arch %s' % (w,))
	


		#print stat i += 1
			#_logger.info('Filieres vides %s' % (fils_empty,))
	
	return ids

apo()
