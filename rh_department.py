from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class rh_department(osv.osv):
	_name = 'rh.department'
	
	def _get_employee_count(self,cr,uid,ids,fields,args,context=None):
			res = {}
			for req in self.browse(cr,uid,ids,context=None):
				if args=="admin":
					res[req.id] = len(req.administrator_ids)
				else:
					res[req.id] = len(req.professor_ids)
			return res
	
	_columns = {
		'name': fields.char("Name",size=128),
		'establishment_id':fields.many2one('rh.establishment', 'Establishment'),
		'leader_id':fields.many2one('rh.employee', 'Leader',domain=[('job_state','=','p')]),
		'secretary_id':fields.many2one('rh.employee','Secretary',domain=[('job_state','!=','p')]),
		'professor_ids': fields.one2many('rh.employee','department_id',string='Professors',domain=[('job_state','=','p')]),
		'administrator_ids': fields.one2many('rh.employee','department_id',string='Administrators',domain=[('job_state','!=','p')]),
		'professor_count':fields.function(_get_employee_count,'prof',type='integer', string='Professors count',store=True),
		'administrator_count':fields.function(_get_employee_count, 'admin',type='integer', string='Administrators count',store=True),
		'logo': fields.binary("Logo of department"),
		'notes': fields.text('Notes'),
		}
rh_department()
