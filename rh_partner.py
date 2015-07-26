from openerp.osv import fields, osv

class rh_users(osv.osv):
    
	_inherit = "res.users"
	_name="res.users"
	_columns = {
		'employee_id':fields.many2one('rh.employee','Employee'),
		}
	def onchage_employee_id(self,cr,uid,ids,id_employee,context=None):
		if id_employee:
			employee_req=self.pool.get('rh.employee')
			for req in self.browse(cr,uid,ids,context):
				for rec in employee_req.browse(cr,uid,[id_employee],context):
					self.write(cr,uid, [req.id],{u'name':rec.complete_name,
												u'image':rec.image,
												u'email':req.email,
												u'active':True})
		else:
			for req in self.browse(cr,uid,ids,context):
				self.write(cr,uid, [req.id],{u'name':'Not Defined',
											u'image':None,
											u'email':None,
											u'active':False})
		return False
rh_users()