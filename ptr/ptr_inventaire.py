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

class ptr_inventaire(osv.osv):

	def _saisie_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'saisie'})
		return True
	def _validation_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'validation'})
		return True
	def _cloture_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'cloture'})
		return True
	def _res_inventaire_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'res_inventaire'})
		return True
	def _rapport_inventaire_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'rapport_inventaire'})
		return True
	def _validation_rp_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'validation_rp'})
		return True

	def _cloture_globale_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'cloture_globale'})
		return True
		
	def _get_date(self, cr, uid, ids, context=None):
			req="SELECT CURRENT_DATE"
			cr.execute(req)
			d=cr.fetchone()[0]
			return d	
	

	def RemplirLigneInventaire(self, cr, uid, ids, context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			tmp1=rec.etablissement.id
			tmp3=rec.id
			tmp4=rec.unite.id
		
		req="SELECT pa.id,geo.unite,pa.ptrgeo,pa.responsable FROM ptr_patrimoineactif pa , ptr_patrimoinegeo geo , ptr_unite u , ptr_etablissement e "\
			"WHERE pa.ptrgeo = geo.id AND geo.unite=u.id AND u.idetablissement= e.id  AND e.id ="+str(tmp1)+" AND u.id ="+str(tmp4)

		cr.execute(req)
		res=cr.fetchall()
		for row in res:
			cr.execute("INSERT INTO ptr_detailinventaire(ptractif,unite,ptrgeo,personne,inventaire) VALUES('"+str(row[0])+"','"+str(row[1])+"','"+str(row[2])+"','"+str(row[3])+"','"+str(tmp3)+"')")
		
	def ViderListe(self, cr, uid, ids, context=None):
		idetab=self.browse(cr,uid,ids,context=None)
		for rec in idetab:
			myid=rec.id
		req="DELETE FROM ptr_detailinventaire WHERE inventaire="+str(myid)
		cr.execute(req)
		cr.execute("UPDATE ptr_inventaire SET nbhorservice='0', nbinexistant='0' WHERE id="+str(myid))
		
		                
                
		
		
	
	_name = 'ptr.inventaire'
	_description = "Classe de l'inventaire"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Lib.'),
		'responsable': fields.char('Resp.'),
		'etablissement':fields.many2one('ptr.etablissement','Etablissement', ondelete='cascade'),
		'unite':fields.many2one('ptr.unite','Departement', ondelete='cascade'),
		'detailinventaire_ids': fields.one2many('ptr.detailinventaire','inventaire',string='LigneInventaire'),
		'nbinexistant':fields.float('nbinexistant'),
		'nbhorservice':fields.float('nbhorservice'),
		'state':fields.selection([
								('saisie','Saisie'),
								('validation','Validation'),
								('cloture','Cloture'),
								('res_inventaire','Resultat inventaire'),
								('rapport_inventaire','Rapport inventaire'),
								('validation_rp','Validation RP'),
								('cloture_globale','Cloture globale'),
								],'State',readonly=True),
					}
					
	_defaults={
	'nbinexistant':'0',
	'nbhorservice':'0',
	'state':'saisie',
	}
	
ptr_inventaire()

