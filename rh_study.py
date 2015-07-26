from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class rh_diploma(osv.osv):
	_name = 'rh.diploma'
	
	def mymod_new(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'new' })
		return True

	def mymod_assigned(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'assigned' })
		return True

	def mymod_negotiation(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'negotiation' })
		return True

	def mymod_won(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'won' })
		return True

	def mymod_reset(self,cr,uid,ids,context):
		self.write(cr, uid, ids, { 'state' : 'new' })
		return 
	def mymod_cancel(self,cr,uid,ids,context):
		self.write(cr, uid, ids, { 'state' : 'canceled' })
		return 


	
		
	_columns = {
		'employee_id': fields.many2one("rh.employee","Employee"),
		'diploma': fields.char("Diploma"),
		'graduation_date': fields.date("Date of graduation"),
		'start_time': fields.datetime("Starting"),
		'establishment': fields.char("Establishment"),
		'city': fields.char("City"),
		'support': fields.binary("Support"),
		'state': fields.selection([
								('new','New'),
								('assigned','Assigned'),
								('negotiation','Negotiation'),
								('won','Won'),
								('canceled','Canceled')
								],'Stage', readonly=False),

			}
rh_diploma()
