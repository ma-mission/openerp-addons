from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from openerp import netsvc

class rh_ordre_mission(osv.osv):
	_name = 'rh.ordre_mission'
	

	def om_validate(self, cr, uid, ids,context=None):
		self.write(cr,uid,ids,{'state':'validated'},context=context)
		wf_service = netsvc.LocalService("workflow")
		for id in ids:
			wf_service.trg_validate(uid, 'rh.ordre_mission',id,'validate', cr)
		return self.om_print_report(cr,uid,ids,context=context)
		 
	def om_confirm(self, cr, uid, ids,context=None):
		self.write(cr, uid, ids, { 'state' : 'confirmed' })
		return True

	def om_paid(self, cr, uid, ids,context=None):
		self.write(cr, uid, ids, { 'state' : 'payed' })
		return True

	def om_cancel(self,cr,uid,ids,context=None):
		self.write(cr, uid, ids, { 'state' : 'canceled' })
		return 

	def om_activate(self, cr, uid, ids,context=None):
		self.write(cr, uid, ids, { 'state' : 'draft' })
		wf_service = netsvc.LocalService("workflow")
		for id in ids:
			wf_service.trg_create(uid, 'rh.ordre_mission', id, cr)
		return True
	
	def om_print_report(self, cr, uid, ids, context=None):
		return {'name':'Ordre de mission',
				'type':'ir.actions.act_window',
				'res_model':'rh.reportwz_om',
				'src_model':'rh.ordre_mission',
				'view_mode':'form',
				'view_type':'form',
				'target':'new'
				}
	
	
	_columns = {
		'doc_ref': fields.char("Ordre de Mission",size=100,readonly=True),
		'employe_ids': fields.many2many("rh.employe","ordre_mission_employe_rel","rh_ordre_mission_id","rh_employe_id",string="Employes"),
		'date_depart':fields.date('Date de Depart'),
		'destination_id':fields.many2one('rh.ville','Destination'),
		'date_retour': fields.date('Date de retour'),
		'nombre_de_jour':fields.integer('Nombre de jours'),
		'moyen_transport_id': fields.many2one('rh.moyen_transport','Moyen de transport'),
		'mission':fields.char('Mission'),
		'prise_en_charge':fields.boolean('Prise en charge'),
		'state': fields.selection([	('draft', 'Draft'), 
									('validated', 'Validated'),
									('confirmed', 'Confirmed'),
									('payed', 'Payed'),
									('canceled', 'Canceled'),
									('reseted', 'Reseted')],
									readonly=True, string='State', track_visibility='onchange'
									),
		'notes': fields.text('Notes'),
		
		}
	_defaults = {
		'state':'draft',
				}
	def create(self, cr, uid, vals, context=None):
			vals['doc_ref'] =  self.pool.get('ir.sequence').get(cr, uid,'rh.ordre_mission_seq',context=context)
			return super(rh_ordre_mission, self).create(cr, uid, vals,context=context)
	
	_rec_name="doc_ref"
rh_ordre_mission()
