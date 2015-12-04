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


class ptr_reglement(osv.osv):
	def create(self, cr, uid, vals, context=None):
		raise osv.except_osv(_('Error!'), _('Seuls les interventions dont le statut est Demande peuvent devenir En Cours.'))
	def ptr_reglement_CheckMontant(self, cr, uid, ids,context=None):
			obj=self.browse(cr,uid,ids,context=None)
			for rec in obj:
				tmp=rec.montant
				if float(tmp)<0 :
					return False
				return True
	def ptr_reglement_CheckSuMantant(self, cr, uid, ids,context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			prestation_id=rec.prestation.id
		cr.execute("SELECT cout FROM ptr_prestation WHERE id="+str(prestation_id))
		prestation_cout=float(cr.fetchone()[0])
		cr.execute("SELECT SUM(montant) AS TOTAL FROM ptr_reglement WHERE prestation="+str(prestation_id))
		montant_sum=float(cr.fetchone()[0])
		if float(prestation_cout)>float(montant_sum):
			cr.execute("UPDATE ptr_prestation SET statut='Payee Partielle' WHERE id="+str(prestation_id))
		if float(prestation_cout)==float(montant_sum):
			cr.execute("UPDATE ptr_prestation SET statut='Payee Totale' WHERE id="+str(prestation_id))
		if float(prestation_cout)<float(montant_sum):
			return False
		return True
		
	_rec_name = 'code'
	_name = 'ptr.reglement'
	_description = "Classe des reglements des prestations"
	_columns = {
        'code': fields.char('Code'),
		'datereglement': fields.date('Date Reglement', required=True),
		'neffet': fields.char('Num. Effet'),
		'dateeffet': fields.date('Date Effet'),
		'montant': fields.float('Montant ttc', required=True),
		'modepaiement':fields.many2one('ptr.modepaiement','Mode Paiement'),
		'banque':fields.many2one('ptr.banque','Banque'),
		'prestation':fields.many2one('ptr.prestation','Prestation', ondelete='cascade'),
		}
	_constraints = [
        (ptr_reglement_CheckMontant, 'Error!\nCertains reglements ont un montant negatif',['montant']),
		(ptr_reglement_CheckSuMantant, 'Error!\nCertains reglements ont depasse le cout de la prestation',['montant'])
		
    ]

ptr_reglement()



