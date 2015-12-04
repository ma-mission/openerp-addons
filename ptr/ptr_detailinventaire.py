from openerp.osv import osv, fields
from openerp import tools

class ptr_detailinventaire(osv.osv):

	def write(self, cr, uid, ids, vals, context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			id_inv=rec.inventaire.id
		if 'existe' in vals:
			cr.execute("SELECT COUNT(*) FROM ptr_detailinventaire WHERE inventaire="+str(id_inv)+" AND UPPER(existe)='NON'")
			tmp=cr.fetchone()[0]
			if tmp is None:
				tmp=0
			cr.execute("UPDATE ptr_inventaire SET nbinexistant="+str(tmp)+" WHERE id="+str(id_inv))
			
		if 'etat' in vals :
			cr.execute("SELECT COUNT(*) FROM ptr_detailinventaire WHERE inventaire="+str(id_inv)+" AND UPPER(etat)='HORS SERVICE'")
			tmp=cr.fetchone()[0]
			if tmp is None:
				tmp=0	
			cr.execute("UPDATE ptr_inventaire SET nbhorservice="+str(tmp)+" WHERE id="+str(id_inv))
			return super(ptr_detailinventaire, self).write(cr, uid, ids, vals, context=context)

	_name = 'ptr.detailinventaire'
	_description = "Classe de detail de l'inventaire"

	_columns = {
		'inventaire':fields.many2one('ptr.inventaire','Inventaire', ondelete='cascade'),
		'ptractif':fields.many2one('ptr.patrimoineactif','ptr Actif'),
		'etat':fields.selection([('NEUF','neuf'), ('BON','bon'), ('MOYEN','moyen'), ('HORS SERVICE','hors service')],string="Etat"),
		'unite':fields.many2one('ptr.unite','Depart.'),
		'ptrgeo':fields.many2one('ptr.patrimoinegeo','ptr geo.'),
		'personne':fields.many2one('rh.employe','User'),
		'existe':fields.selection([('OUI','oui'), ('NON','non')],string="Existant"),
		'observation':fields.char('Observation'),
					}
	_defaults = {
		'existe' : 'OUI'
		}
	_sql_constraints = [
        ('number_uniq', 'unique(inventaire, ptractif)','Impossible de doubler un patrimoin actif dans le meme inventaire')
	    
    ]	    
		
ptr_detailinventaire()

