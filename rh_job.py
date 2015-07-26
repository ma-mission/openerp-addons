from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class rh_job(osv.osv):
	_name = 'rh.job'

	_columns = {
		'employee_id': fields.many2one('rh.employee','Employee'),
		'poste_id': fields.many2one("rh.poste","Poste"),
		'category': fields.char("Category",size=128),
		'scale': fields.integer("Scale"),
		'echelon': fields.integer("Echelon"),
		'index': fields.integer("Index"),
		'scale_effect_date': fields.date("Date of scale effect"),
		'echelon_effect_date': fields.date("Date of scale effect"),
		'support': fields.binary("Support"),
		'current_state':fields.boolean("Is current state?"),
		'job_state':fields.selection((('a','Administrator'), ('p','Professor'),('d','Detached'),('t','Temporary')),
			'Job State'),
			}
	def onchange_current_state(self,cr,uid,ids,args,context):
		job_ids=self.search(cr,uid,[('employee_id','=',args)])
		for req in self.browse(cr,uid,job_ids,context):
			if req.id not in ids:
				self.write(cr,uid, [req.id],{u'current_state':False,u'onchange':True})
		return False
		
	def create(self, cursor, user, vals, context=None):
		if 'category' in vals:
			vals['category'] = vals['category'].title()
		id=super(rh_job, self).create(cursor, user, vals,context=context)
		#update poste count
		obj=self.pool.get('rh.poste')
		poste_ids=obj.search(cursor, user,[])
		for req in obj.browse(cursor, user,poste_ids,context):
			obj.write(cursor, user, req.id,{'name':req.name})
		#update employee job
		obj=self.pool.get('rh.employee')
		for req in self.browse(cursor,user,[id],context):
			obj.write(cursor, user,[req.employee_id.id],{'name':req.employee_id.name})
		return id
			
	def write(self, cursor, user, ids, vals, context=None):
		if 'category' in vals:
			vals['category'] = vals['category'].title()
		id=super(rh_job, self).write(cursor, user, ids, vals,context=context)
		#update employee job
		if not 'onchange' in vals:
			obj=self.pool.get('rh.employee')
			for req in self.browse(cursor,user,ids,context):
				obj.write(cursor, user,[req.employee_id.id],{'name':req.employee_id.name})
		else:
			del vals['onchange']
		#update poste count
		obj=self.pool.get('rh.poste')
		poste_ids=obj.search(cursor, user,[])
		for req in obj.browse(cursor, user,poste_ids,context):
			obj.write(cursor, user, req.id,{'name':req.name})
		return id
rh_job()



class rh_poste(osv.osv):
	
	_name = 'rh.poste'
	def _get_poste_count(self,cr,uid,ids,fields,args,context):
		res = {}
		icount = 0
		for record in self.browse(cr,uid,ids,context) :
			for req in record.poste_ids:
				if req.current_state:
					icount=icount+1
			res[record.id] = icount
		return res
	_columns = {
		'name': fields.char("Name",size=128),
		'poste_ids': fields.one2many("rh.job","poste_id","Postes"),
		'poste_count':fields.function(_get_poste_count, type='integer', string='Poste count',store=True),
		
		}
	def write(self, cursor, user, ids, vals, context=None):
		return super(rh_poste, self).write(cursor, user, ids, vals,context=context)
	
rh_poste()
