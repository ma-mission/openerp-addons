from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import logging



class rh_demande(osv.osv):
	_name = 'rh.demande'
	_inherit = 'ir.needaction_mixin'
	def _needaction_domain_get (self, cr, uid, context = None):
		if self._needaction:
			return [('state', '=', True)]
		return []

	_columns = {
		'doc_ref':fields.char('Reference', size=64),
		'employe_id': fields.many2one('rh.employe','Full name'),
		'demande': fields.char("request",size=100),
		'date': fields.date("Date"),
		'state':fields.boolean("State"),
		'reason': fields.char("Reason"),
		'adress': fields.text("Adress"),
		'start_date': fields.date("Start date"),
		'end_date': fields.date("End date"),
		'ville_id': fields.many2one("rh.ville"),
		}
	_defaults = {
			 'state':True,
			 'date': fields.date.context_today,
			}
	
	def print_report(self, cr, uid, ids, context=None):
		for req in self.browse(cr,uid,ids,context=None):
			if req.state == True:
				self.write(cr,uid, req.id,{'state':False})
				obj = self.pool.get('rh.employe')
				datas = {
						'ids': [req.employe_id.id],
						'model':'rh.employee',
						'form':self.read(cr, uid,ids)[0]
						}
				if req.demande == 'AT':
					return {
						'report_name': 'rh.employe.attestation_travail_webkit',
						'type': 'ir.actions.report.xml',
						'datas': datas,
						
						}
				elif req.demande == 'AQT':
					return {
						'report_name': 'rh.employe.autorisation_quittement_territoire_webkit',
						'type': 'ir.actions.report.xml',
						'datas': datas,
						}
						
				elif req.demande == 'AS':
					return {
						'report_name': 'rh.employe.attestation_salaire_webkit',
						'type': 'ir.actions.report.xml',
						'datas': datas,
						
						}
					
			else:
				raise osv.except_osv(('Worning:'), ('Action already done! ' ) )
				return False
   	def create(self, cr, uid, vals, context=None):
			vals['doc_ref'] =  self.pool.get('ir.sequence').get(cr, uid,'rh.demande_seq',context=context)
			return super(rh_demande, self).create(cr, uid, vals,context=context)
	
	
	_order='date'
rh_demande();



