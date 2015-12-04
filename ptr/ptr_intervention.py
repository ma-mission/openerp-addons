import csv
import psycopg2
import openerp.exceptions
from openerp.osv import osv, fields,orm
from openerp import tools
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _


class ptr_intervention(osv.osv):

	def dep_onchange(self, cr, uid, ids, args, context=None):
		res={}
		obj=self.pool.get("ptr.patrimoinegeo")
		geo_ids=obj.search(cr,uid,[('unite','=',args)])
		return {'value': {
            'ptrgeo': geo_ids
            }
        }
	def _get_date(self, cr, uid, ids, context=None):
		req="SELECT CURRENT_DATE"
		cr.execute(req)
		d=cr.fetchone()[0]
		return d

	def Statut_EnCours(self, cr, uid, ids, context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			tmp1=rec.id
			tmp2=rec.statut
		req="SELECT CURRENT_DATE"
		cr.execute(req)
		d=cr.fetchone()[0]
		if str(tmp2) == 'Demande' :
			cr.execute("UPDATE ptr_intervention SET statut='En Cours', dateencours='"+str(d)+"' WHERE id ="+str(tmp1))
		else :
			raise osv.except_osv(_('Error!'), _('Seuls les interventions dont le statut est Demande peuvent devenir En Cours.'))
		
	def Statut_Executee(self, cr, uid, ids, context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			tmp1=rec.id
			tmp2=rec.statut
		req="SELECT CURRENT_DATE"
		cr.execute(req)
		d=cr.fetchone()[0]
		if str(tmp2) == 'En Cours' :
			cr.execute("UPDATE ptr_intervention SET statut='Executee', dateexeute='"+str(d)+"' WHERE id ="+str(tmp1))
		else :
			raise osv.except_osv(_('Error!'), _('Seuls les interventions dont le statut est En Cours peuvent devenir Executee.'))
	

	
	_name = 'ptr.intervention'
	_description = "Classe de l' intervention"
	_rec_name = 'libelle'

	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Lib.', required=True),
		'probleme': fields.text('Probleme'),
		'diagnostic': fields.text('Diagnostic'),
		'solution': fields.text('Solution'),
		'datedemande': fields.date('DateDem.'),
		'dateencours': fields.date('DateCours'),
		'dateexeute': fields.date('DateExec.'),
		'volh':fields.float('Vol.Horaire'),
		'coutprestation':fields.float('Cout Presta.'),
		'statut':fields.char('Statut'),
		'etablissement':fields.many2one('ptr.etablissement','Etablissement', ondelete='cascade'),
		'unite':fields.many2one('ptr.unite','Departem.'),
		'ptractif':fields.many2one('ptr.patrimoineactif','ptr Actif', required=True),
		'ptrgeo':fields.many2one('ptr.patrimoinegeo','ptr Geo.', required=True),
		'personnel':fields.many2one('rh.employe','Resp.', required=True),
		'priorite':fields.many2one('ptr.priorite','Priorite'),
		'technicien_ids': fields.one2many('ptr.technicieninterne','intervention',string='Technicien Interne'),
		'prestation_ids': fields.one2many('ptr.prestation','intervention',string='Prestation'),

					}
	_defaults = {
		'statut' : 'Demande',
		'datedemande':_get_date,
		'coutprestation':'0',
		}
	
ptr_intervention()

