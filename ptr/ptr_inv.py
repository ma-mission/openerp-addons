from openerp import addons

from openerp.osv import fields, osv

from openerp import tools

class ptr_inv(osv.osv):
	def _draft_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'draft'})
		return True
	
	def _redaction_pv_lancement_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'redaction_pv_lancement'})
		return True
	def _signature_courrier_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'signature_courrier'})
		return True
	def _designation_equipe_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'designation_equipe'})
		return True
	def _maj_plan_action_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'maj_plan_action'})
		return True
	def _diffusion_rpe_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'diffusion_rpe'})
		return True
	def _pv_reunion_ouverture_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'pv_reunion_ouverture'})
		return True
	def _demarrage_inventaire_fcn(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'state':'demarrage_inventaire'})
		cr.execute("SELECT id FROM ptr_etablissement")
		res=cr.fetchall()
		for row in res:
			cr.execute("INSERT INTO ptr_inventaire(etablissement,state,unite)VALUES('"+str(row[0])+"','saisie','1')")
		return True
		
	_name = 'ptr.inv'
	_description = " Porcessus d inventaire"

	_columns = {
			'name':fields.char('Name'),
			'date_inv_dec':fields.date('Date de declenchement'),
			'date_inv_ar':fields.date('Date d arret'),
			'state':fields.selection([
											('draft','Draft'),
											('redaction_pv_lancement','Redaction du PV de lancement'),
											('signature_courrier','Validation et signature de courrier'),
											('designation_equipe','Designation de l equipe d inventaire'),
											('maj_plan_action','MAJ plan d action'),
											('diffusion_rpe','Diffusion RPE'),
											('pv_reunion_ouverture','PV de reunion ouverture'),
											('demarrage_inventaire','Demarrage inventaire'),
											],'State',readonly=True),

			}

ptr_inv()

