from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools





class rh_salary(osv.osv):
	
	_name = 'rh.salary'
	_columns = {
		'employe_id': fields.many2one("rh.employe","Employe"),
		'rubrique_id': fields.many2one("rh.rubrique","Rubric"),
		'price': fields.float("Price"),
		'mois':fields.selection([
								 ('01', 'Janvier'),
								 ('02', 'Fevrier'),
								 ('03', 'Mars'),
								 ('04', 'Avril'),
								 ('05', 'Mai'),
								 ('06', 'Juin'),
								 ('07', 'Juillet'),
								 ('08', 'Aout'),
								 ('09', 'Septembre'),
								 ('10', 'Octobre'),
								 ('11', 'Nevembre'),
								 ('12', 'Decembre')
								  ], 'Mois'),
		'annee':fields.integer("Annee"),
		}
	def create(self, cursor, user, vals, context=None):
		if 'annee' in vals:
			annee_ids=[]
			annee=vals['annee']
			obj=self.pool.get("rh.annee")
			annee_ids=obj.search(cursor, user, [('annee', '=', annee)],context=None)
			if annee_ids == [] :
				obj.create(cursor,user,{'annee':annee},context=None)
		return super(rh_salary, self).create(cursor, user, vals,context=context)
	
	def write(self, cursor, user, ids, vals, context=None):
		if 'annee' in vals:
			last_vals={}
			annee_ids=[]
			annee=vals['annee']
			obj=self.pool.get("rh.annee")
			annee_ids=obj.search(cursor, user, [('annee', '=', annee)],context=None)
			if annee_ids == [] :
				obj.create(cursor,user,{'annee':annee},context=None)
			last_vals=self.read(cursor,user,ids)
			if not annee == last_vals[0]['annee']:
				if not 'employe_id' in vals:
					vals['employe_id']=last_vals[0]['employe_id'][0]
				if not 'rubrique_id' in vals:
					vals['rubrique_id']=last_vals[0]['rubrique_id'][0]
				if not 'price' in vals:
					vals['price']=last_vals[0]['price']
				if not 'mois' in vals:
					vals['mois']=last_vals[0]['mois']
				return super(rh_salary, self).create(cursor, user, vals,context=context)
		if 'mois' in vals:
			last_vals={}
			last_vals=self.read(cursor,user,ids)
			if not vals['mois'] == last_vals[0]['mois']:
				if not 'employe_id' in vals:
					vals['employe_id']=last_vals[0]['employe_id'][0]
				if not 'rubrique_id' in vals:
					vals['rubrique_id']=last_vals[0]['rubrique_id'][0]
				if not 'price' in vals:
					vals['price']=last_vals[0]['price']
				if not 'annee' in vals:
					vals['annee']=last_vals[0]['annee']
				return super(rh_salary, self).create(cursor, user, vals,context=context)
		
		return super(rh_salary, self).write(cursor, user, ids, vals,context=context)

rh_salary();