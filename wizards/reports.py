from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import logging
_logger = logging.getLogger(__name__)


class rh_reportwzLC(osv.osv_memory):
	_name = "rh.reportwzlc"
   
	def _get_active_address(self, cr, uid, context):
		if context.get('active_model') == 'rh.employee':
			obj = self.pool.get('rh.employee')
			for record in obj.browse(cr, uid, context.get('active_ids'), context):
				return " %s, %s" %(record.adress,  record.city)
		return False
	_columns = {
			'reason': fields.char("Reason"),
			'adress': fields.text("Adress"),
			'start_date': fields.date("Start date"),
			'end_date': fields.date("End date"),
					}
	_defaults = {
			 'adress': _get_active_address,
					}
	def print_report(self, cr, uid, ids, context):
		for req in self.browse(cr,uid,ids,context):
			ctx_id=context.get('active_id')
			obj=self.pool.get('rh.employee.request')
			id=obj.create(cr,uid,{ 'applicant_id':ctx_id,
								'request':'Autorisationn de quittement du territoire national',
								'state':False,
								'reason':req.reason,
								'adress':req.adress,
								'start_date':req.start_date,
								'end_date':req.end_date}
								,context)
			datas = {
					'ids':[ctx_id],
					'model':'rh.employee',
					'form':obj.read(cr, uid,[id])[0]
					}
			return {
					'report_name': 'rh.employee.leave_country_webkit',
					'type': 'ir.actions.report.xml',
					'datas': datas,
					
					}
rh_reportwzLC()

class rh_reportwzAC(osv.osv_memory):
	_name = "rh.reportwzac"
   
	def print_report(self, cr, uid, ids, context):
		ctx_id=context.get('active_id')
		obj=self.pool.get('rh.employee.request')
		id=obj.create(cr,uid,{ 'applicant_id':ctx_id,
							'request':'Attestation administrative',
							'state':False,
								}
							,context)
		datas = {
				'ids':[ctx_id],
				'model':'rh.employee',
				'form':obj.read(cr, uid,[id])[0]
				}
		return {
				'report_name': 'rh.employee.administrative_certification_webkit',
				'type': 'ir.actions.report.xml',
				'datas': datas,
				}
rh_reportwzAC()


