from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class rh_fonction(osv.osv):

	def onchange_category(self,cr,uid,ids, arg,context=None):
			obj = self.pool.get('rh.fonction.corps')
			new_ids = obj.search(cr,uid, [('category_id','=',arg)],context)
			return {'domain':{'corps_id':[('id','in',new_ids)]},'value':{'corps_id':new_ids[0]}}
	def onchange_corps(self,cr,uid,ids, arg,context=None):
			obj = self.pool.get('rh.fonction.cadre')
			new_ids = obj.search(cr,uid, [('corps_id','=',arg)],context)
			return {'domain':{'cadre_id':[('id','in',new_ids)]},'value':{'cadre_id':new_ids[0]}}
	def onchange_cadre(self,cr,uid,ids, arg,context=None):
			obj = self.pool.get('rh.fonction.grade')
			new_ids = obj.search(cr,uid, [('cadre_id','=',arg)],context)
			return {'domain':{'grade_id':[('id','in',new_ids)]},'value':{'grade_id':new_ids[0]}}
	def onchange_grade(self,cr,uid,ids, arg,context=None):
			obj = self.pool.get('rh.fonction.echelon')
			new_ids = obj.search(cr,uid, [('grade_id','=',arg)],context)
			if new_ids:
				return {'domain':{'echelon_id':[('id','in',new_ids)]},'value':{'echelon_id':new_ids[0]}}
			return {'domain':{'echelon_id':[('id','in',new_ids)]}}
	def _get_function_code(self, cr, uid, ids, name, arg, context=None):
			res = {}
			for fnc in self.browse(cr, uid, ids, context=context):
				res[fnc.id] = fnc.grade_id.code
			return res	
	
	_name = 'rh.fonction'

	_columns = {
		'code':fields.function(_get_function_code,type="char", method=True, string="Code"),
		'employe_id': fields.many2one('rh.employe','Employe'),
		'category_id': fields.many2one("rh.fonction.category","Category"),
		'corps_id': fields.many2one("rh.fonction.corps","Corps"),
		'cadre_id': fields.many2one("rh.fonction.cadre","Cadre"),
		'grade_id': fields.many2one("rh.fonction.grade","Grade"),
		'echelon_id': fields.many2one("rh.fonction.echelon","Echelon"),
		'grade_date': fields.date("Date de Grade"),
		'echelon_date': fields.date("Date d echelon"),
		'deduction': fields.integer("Deductions"),
		'support': fields.binary("Support"),
		'ville_id': fields.many2one("rh.ville","Ville"),
		'state':fields.selection([('A','Active'), ('I','Inactive'),('P','Proposed')], "State"),
		'notes': fields.text('Notes'),
		 }
	_default = {
		}
	def create(self, cursor, user, vals, context=None):
		if vals['state']=='A':
			lines=[]
			emp_id=vals['employe_id']
			self.pool.get("rh.employe").write(cursor,user,emp_id,{'echelon_date_rel':vals['echelon_date'],'deduction_rel':vals['deduction'] or 0,'grade_id':vals['grade_id'],'cadre_id':vals['cadre_id'],'corps_id':vals['corps_id'],'category_id':vals['category_id'] },context=context)
			lines=self.search(cursor,user, [('employe_id','=',emp_id)],context=context)
			for line in lines:
				if self.read(cursor,user,line)['state'] == 'A':
					self.write(cursor,user,line,{'state':'I'},context=context)
		
		return super(rh_fonction, self).create(cursor, user, vals,context=context)
			
	
	def write(self, cursor, user, ids, vals, context=None):
		if vals['state']=='A':
			lines=[]
			if 'employe_id' in vals:
				emp_id=vals['employe_id']
			else:
				emp_id=self.read(cursor,user,ids[0])['employe_id'][0]
				print emp_id
			if 'echelon_date' in vals:
				date=vals['echelon_date']
			else:
				date=self.read(cursor,user,ids[0])['echelon_date']
			if 'deduction' in vals:
				deduction=vals['deduction']
			else:
				deduction=self.read(cursor,user,ids[0])['deduction']
			if 'category_id'in vals:
				grade_id=vals['category_id']
			else:
				category_id=self.read(cursor,user,ids[0])['category_id']
			if 'corps_id'in vals:
				corps_id=vals['corps_id']
			else:
				corps_id=self.read(cursor,user,ids[0])['corps_id']
			if 'cadre_id'in vals:
				grade_id=vals['cadre_id']
			else:
				cadre_id=self.read(cursor,user,ids[0])['cadre_id']
			if 'grade_id'in vals:
				grade_id=vals['grade_id']
			else:
				grade_id=self.read(cursor,user,ids[0])['grade_id']
			self.pool.get("rh.employe").write(cursor,user,emp_id,{'echelon_date_rel':date,'deduction_rel':deduction,'grade_id':grade_id,'corps_id':corps_id,'cadre_id':cadre_id,'category_id':category_id},context=context)
			lines=self.search(cursor,user, [('employe_id','=',emp_id)],context=context)
			for line in lines:
				if self.read(cursor,user,line)['state'] == 'A':
					self.write(cursor,user,line,{'state':'I'},context=context)
		return super(rh_fonction, self).write(cursor, user, ids, vals,context=context)
	_order = "grade_id"
	_rec_name="grade_id"
rh_fonction()

