from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from openerp import netsvc


class rh_reportwz_aqt(osv.osv_memory):
	_name = "rh.reportwz_aqt"
   
	def _get_active_address(self, cr, uid, context):
		if context.get('active_model') == 'rh.employe':
			obj = self.pool.get('rh.employe')
			for record in obj.browse(cr, uid, context.get('active_ids'), context):
				return " %s" %(record.adress)
	def _get_active_ville(self, cr, uid, context=None):
		res={}
		if context.get('active_model') == 'rh.employe':
			obj = self.pool.get('rh.employe')
			for record in obj.browse(cr, uid, context.get('active_ids'), context):
				return record.city_id.id
		return False
	_columns = {
			'reason': fields.char("Reason"),
			'adress': fields.text("Adress"),
			'update_adress': fields.boolean("Update Address"),
			'start_date': fields.date("Start date"),
			'end_date': fields.date("End date"),
			'ville_id': fields.many2one("rh.ville","Ville"),
					}
	_defaults = {
			 'adress': _get_active_address,
			 'ville_id': _get_active_ville,
			 	}
	def print_report(self, cr, uid, ids, context):
		for req in self.browse(cr,uid,ids,context):
			ctx_id=context.get('active_id')
			if req.update_adress:
				self.pool.get('rh.employe').write(cr,uid,ctx_id,{'city_id':req.ville_id.id,'adress':req.adress},context=context)
			obj=self.pool.get('rh.demande')
			id=obj.create(cr,uid,{ 'employe_id':ctx_id,
								'demande':'AQT',
								'state':False,
								'reason':req.reason,
								'adress':req.adress,
								'start_date':req.start_date,
								'end_date':req.end_date,
								'ville_id':req.ville_id.id,
								}
								,context)
			datas = {
					'ids':[ctx_id],
					'model':'rh.employe',
					'form':obj.read(cr, uid,[id])[0]
					}
			return {
					'report_name': 'rh.employe.autorisation_quittement_territoire_webkit',
					'type': 'ir.actions.report.xml',
					'datas': datas,
					
					}
rh_reportwz_aqt()

class rh_reportwz_at(osv.osv_memory):
	_name = "rh.reportwz_at"
   
	def print_report(self, cr, uid, ids, context):
		ctx_id=context.get('active_id')
		obj=self.pool.get('rh.demande')
		id=obj.create(cr,uid,{ 'employe_id':ctx_id,
							'demande':'AT',
							'state':False,
								}
							,context)
		datas = {
				'ids':[ctx_id],
				'model':'rh.employe',
				'form':obj.read(cr, uid,[id])[0]
				}
		return {
				'report_name': 'rh.employe.attestation_travail_webkit',
				'type': 'ir.actions.report.xml',
				'datas': datas,
				}
rh_reportwz_at()

class rh_reportwz_as(osv.osv_memory):
	_name = "rh.reportwz_as"
   
	def print_report(self, cr, uid, ids, context):
		ctx_id=context.get('active_id')
		obj=self.pool.get('rh.demande')
		id=obj.create(cr,uid,{ 'employe_id':ctx_id,
							'demande':'AS',
							'state':False,
								}
							,context)
		datas = {
				'ids':[ctx_id],
				'model':'rh.employe',
				'form':obj.read(cr, uid,[id])[0]
				}
		return {
				'report_name': 'rh.employe.attestation_salaire_webkit',
				'type': 'ir.actions.report.xml',
				'datas': datas,
				}
rh_reportwz_as()

class rh_reportwz_om(osv.osv_memory):
	_name = "rh.reportwz_om"
   
	def print_report(self, cr, uid, ids, context):
		ctx_id=context.get('active_id')
		datas = {
				'ids':[ctx_id],
				'model':'rh.ordre_mission',
				}
		return {
				'report_name': 'rh.ordre_mission.ordre_mission_webkit',
				'type': 'ir.actions.report.xml',
				'datas': datas,
				}
rh_reportwz_om()
