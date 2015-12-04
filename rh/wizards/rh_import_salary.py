from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import csv
import base64

class rh_import_salary_wz(osv.osv_memory):
	_name = "rh.import_salary_wz"
   
	def _get_active_address(self, cr, uid, context):
		if context.get('active_model') == 'rh.employee':
			obj = self.pool.get('rh.employee')
			for record in obj.browse(cr, uid, context.get('active_ids'), context):
				return " %s, %s" %(record.adress,  record.city)
		return False
	_columns = {
			'mois':fields.selection([
								 ('01', 'Janvier'),
								 ('02', 'Fevrier'),
								 ('03', 'Mars'),
								 ('04', 'Avril'),
								 ('05', 'Mai'),
								 ('06', 'Juin'),
								 ('07', 'Juillet'),
								 ('08', 'Aout'),
								 ('09', 'Septembre'),
								 ('10', 'Octobre'),
								 ('11', 'Nevembre'),
								 ('12', 'Decembre')
								  ], 'Mois'),
			'annee': fields.integer("Annee"),
			'fichier': fields.binary("Fichier"),
			
			
					}
	_defaults = {
			
					}

	def import_salary(self, cr, uid, ids, context=None):
		vals={}
		vals1={}
		emp_id=0
		employe_obj=self.pool.get("rh.employe")
		rubrique_obj=self.pool.get("rh.rubrique")
		salary_obj=self.pool.get("rh.salary")
		annee_obj=self.pool.get("rh.annee")
		for record in self.browse(cr,uid,ids,context=context):
			lines=base64.b64decode(record.fichier)
			lines=lines.splitlines()
			for line in lines:
				if '|' in line:
					cols=line.split('|')
					emp_ids=employe_obj.search(cr,uid,[('som','=',cols[0])],context=context)
					emp_id=emp_ids[0] if (type(emp_ids)==list) & (len(emp_ids)!=0) else emp_ids
					if emp_id:
						rubrique_ids=rubrique_obj.search(cr,uid,[('code','=',cols[1])],context=context)
						annee_ids=annee_obj.search(cr,uid,[('annee','=',record.annee)],context=context)
						vals['rubrique_id']=rubrique_ids[0] if (type(rubrique_ids)==list) & (len(rubrique_ids)!=0) else rubrique_ids
						vals['employe_id']=emp_id
						vals['price']=cols[2]
						vals['mois']=vals1['mois']=record.mois
						vals['annee']=record.annee
						vals1['annee_id']=annee_ids[0] if (type(annee_ids)==list) & (len(annee_ids)!=0) else annee_ids
						
						salary_obj.create(cr,uid,vals,context=context)
						employe_obj.write(cr,uid,emp_id,vals1,context=context)

		return True
rh_import_salary_wz()

