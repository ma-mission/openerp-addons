from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import csv
import base64
import time

class rh_import_data_wz(osv.osv_memory):
	_name = "rh.import_data_wz"
   
	_columns = {
			'fichier': fields.binary("Fichier"),
			'ville_id': fields.many2one("rh.ville", "Ville"),
			'import_static_info': fields.boolean("Import static info"),
			
					}
	_defaults = {
			
					}

	def import_data(self, cr, uid, ids, context):
		vals={}
		emp_ids=[]
		emp_id=0
		last_date=0
		pays_obj=self.pool.get('res.country')
		employe_obj=self.pool.get("rh.employe")
		fonction_obj=self.pool.get("rh.fonction")
		category_obj=self.pool.get("rh.fonction.category")
		corps_obj=self.pool.get("rh.fonction.corps")
		cadre_obj=self.pool.get("rh.fonction.cadre")
		grade_obj=self.pool.get("rh.fonction.grade")
		echelon_obj=self.pool.get("rh.fonction.echelon")
		for record in self.browse(cr,uid,ids,context=context):
			lines=base64.b64decode(record.fichier)
			lines=lines.splitlines()
			for line in lines:
				if '|' in line:
					cols=line.split('|')
					emp_id=employe_obj.search(cr,uid,[('som','=',cols[0])],context=context)
					if len(cols):
						if len(emp_id):
							if record['import_static_info']:
								cols[2]=cols[2].strip()
								cols[2]=cols[2].split(' ')
								vals['lastname']=cols[2][len(cols[2])-1]
								del cols[2][len(cols[2])-1]
								s=''
								for x in cols[2]:
									s=s+x+' '
								vals['name']=s
								vals['som']=cols[0]
								vals['cin']=cols[1]
								vals['gender']=cols[3]
								vals['pays_id']=pays_obj.search(cr,uid,[('code','=',cols[4])],context=context)[0]
								s=cols[5].strip(' ')
								if len(s)==4:
									vals['birthday']=s+'-01-01'
									vals['birthday_state']=True
								else:
									s=s.ljust(6,'0')
									vals['birthday']=s[4:8]+'-'+s[2:4]+'-'+s[0:2]
									vals['birthday_state']=False
								s=cols[6]
								vals['recrutement_date']=s[6:10]+'-'+s[3:5]+'-'+s[0:2]
							vals['marital']=cols[16]
							vals['num_children']=cols[17]
							vals['organisme_id']=cols[7]
							employe_obj.write(cr,uid,emp_id,vals,context=context)
							emp_ids.append(emp_id)
						else:
							cols[2]=cols[2].strip()
							cols[2]=cols[2].split(' ')
							vals['lastname']=cols[2][len(cols[2])-1]
							del cols[2][len(cols[2])-1]
							s=''
							for x in cols[2]:
								s=s+x+' '
							vals['name']=s
							vals['som']=cols[0]
							vals['cin']=cols[1]
							vals['gender']=cols[3]
							vals['pays_id']=pays_obj.search(cr,uid,[('code','=',cols[4])],context=context)[0]
							s=cols[5].strip(' ')
							if len(s)==4:
								vals['birthday']=s+'-01-01'
								vals['birthday_state']=True
							else:
								s=s.ljust(6,'0')
								vals['birthday']=s[4:8]+'-'+s[2:4]+'-'+s[0:2]
								vals['birthday_state']=False
							s=cols[6]
							vals['recrutement_date']=s[6:10]+'-'+s[3:5]+'-'+s[0:2]
							vals['marital']=cols[16]
							vals['num_children']=cols[17]
							vals['organisme_id']=cols[7]
							emp_id=[]
							emp_id.append(employe_obj.create(cr,uid,vals,context=context))
							emp_ids.append(emp_id[0])
							emp_id
						last_date_tmp=employe_obj.browse(cr,uid,emp_id,context=context)
						if  last_date_tmp[0]['echelon_date_rel']:
							last_date=last_date_tmp[0]['echelon_date_rel']
						else:
							last_date='1975-01-01'
						s=cols[9]
						new_date=s[6:10]+'-'+s[3:5]+'-'+s[0:2]
						if time.strptime(last_date, "%Y-%m-%d") < time.strptime(new_date, "%Y-%m-%d"):
							vals={}
							vals['echelon_date']=new_date
							s=cols[10]
							vals['category_id']=category_obj.search(cr,uid,[('code','=',s[0:2])],context=context)[0]
							vals['corps_id']=corps_obj.search(cr,uid,[('code','=',s[0:4])],context=context)[0]
							vals['cadre_id']=cadre_obj.search(cr,uid,[('code','=',s[0:6])],context=context)[0]
							vals['grade_id']=grade_obj.search(cr,uid,[('code','=',s[0:8])],context=context)[0]
							fonction_ids=[]
							fonction_ids=fonction_obj.search(cr,uid,[('employe_id','=',emp_id[0])],context=context)
							if fonction_ids==[]:
								vals['grade_date']=new_date
							for fcn_rec in fonction_obj.browse(cr,uid,fonction_ids,context=context):
								if fcn_rec['state']=='A' :
									last_code=fcn_rec['grade_id'].code
									new_code=int(s[0:8])
									if (last_code - new_code):
										vals['grade_date']=new_date
									else:
										vals['grade_date']=fcn_rec['grade_date']
							s=cols[12].strip(' ')
							s1=cols[13].strip(' ')
							s2=echelon_obj.search(cr,uid,[('code','=',s1),('echelon','=',s),('grade_id','=',vals['grade_id'])],context=context)
							if not len(s2):
								vals['echelon_id']=echelon_obj.create(cr, uid, {'code':s1,'echelon':s,'grade_id':vals['grade_id']},context=context)
							else:
								vals['echelon_id']=s2[0]
							vals['employe_id']=emp_id[0]
							vals['state']='A'
							vals['ville_id']=record['ville_id'].id
							vals['deduction']=int(cols[18].strip(' '))
							fonction_obj.create(cr, uid, vals,context=context)
						
		return {
				'name': 'Imported Employes',
				'view_type': 'form',
				'view_mode': 'tree,form',
				'res_model': 'rh.employe',
				'context': "{}",
				'domain': [('id','in',emp_ids)],
				'type': 'ir.actions.act_window',
				'nodestroy': False,
				
                }
rh_import_data_wz()

