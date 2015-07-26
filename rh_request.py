from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import logging
_logger = logging.getLogger(__name__)



class rh_employee_request(osv.osv):
	_name = 'rh.employee.request'
	_inherit = 'ir.needaction_mixin'
	def _needaction_domain_get (self, cr, uid, context = None):
		if self._needaction:
			return [('state', '=', True)]
		return []

	_columns = {
		'doc_ref':fields.char('Reference', size=64),
		'applicant_id': fields.many2one('rh.employee','Full name'),
		'request': fields.char("request",size=100),
		'date': fields.date("Date"),
		'state':fields.boolean("State"),
		'reason': fields.char("Reason"),
		'adress': fields.text("Adress"),
		'start_date': fields.date("Start date"),
		'end_date': fields.date("End date"),
		}
	_defaults = {
			 'state':True,
			 'date': fields.date.context_today,
			 'doc_ref': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid,'rh.employee.request'),
					}
	
	def print_report(self, cr, uid, ids, context=None):
		for req in self.browse(cr,uid,ids,context=None):
			if req.state == True:
				self.write(cr,uid, req.id,{'state':False})
				obj = self.pool.get('rh.employee')
				datas = {
						'ids': [req.applicant_id.id],
						'model':'rh.employee',
						'form':self.read(cr, uid,ids)[0]
						}
				if req.request == 'Attestation administrative':
					return {
						'report_name': 'rh.employee.administrative_certification_webkit',
						'type': 'ir.actions.report.xml',
						'datas': datas,
						
						}
				elif req.request == 'Autorisationn de quittement du territoire national':
					return {
						'report_name': 'rh.employee.leave_country_webkit',
						'type': 'ir.actions.report.xml',
						'datas': datas,
						
						}
					
			else:
				raise osv.except_osv(('Worning:'), ('Action already done! ' ) )
				return False
   	
	_order='date'
rh_employee_request();



