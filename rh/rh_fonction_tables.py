from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools



class rh_fonction_category(osv.osv):
	
	_name = 'rh.fonction.category'
	_columns = {
		'name': fields.char("Name",size=128),
		'code': fields.char("Code",size=2),
		'corps_ids': fields.one2many("rh.fonction.corps","category_id","Corps"),
		}
rh_fonction_category();


class rh_fonction_corps(osv.osv):
	
	_name = 'rh.fonction.corps'
	_columns = {
		'category_id': fields.many2one("rh.fonction.category","Category"),
		'name': fields.char("Name",size=128),
		'code': fields.char("Code",size=4),
		'cadre_ids': fields.one2many("rh.fonction.cadre","corps_id","Cadres"),
		}
rh_fonction_corps();

class rh_fonction_cadre(osv.osv):
	
	_name = 'rh.fonction.cadre'
	_columns = {
		'corps_id': fields.many2one("rh.fonction.corps","Corps"),
		'name': fields.char("Name",size=128),
		'code': fields.char("Code",size=6),
		'grade_ids': fields.one2many("rh.fonction.grade","cadre_id","Grades"),
		}
rh_fonction_cadre();

class rh_fonction_grade(osv.osv):
	
	_name = 'rh.fonction.grade'
	_columns = {
		'cadre_id': fields.many2one("rh.fonction.cadre","Cadre"),
		'name': fields.char("Name",size=128),
		'code': fields.integer("Code",size=8),
		'scale':fields.integer("Scale",size=2),
		'echelon_ids': fields.one2many("rh.fonction.echelon","grade_id","Echelons"),
		}
rh_fonction_grade();

class rh_fonction_echelon(osv.osv):
	
	_name = 'rh.fonction.echelon'
	def _echelon_name_get_fnc(self, cr, uid, ids, args=None,fields=None,context=None):
			res = {}
			tmp_str=''
			for record in self.browse(cr, uid, ids, context=context):
				if record.code:
					tmp_str= record.code
				if record.echelon:
					tmp_str= str(tmp_str)+'-'+str(record.echelon)
				res[record.id]=tmp_str
				tmp_str=''
			return res
	_columns = {
		'grade_id': fields.many2one("rh.fonction.grade","Garde"),
		'name': fields.function(_echelon_name_get_fnc, type="char", string="Name",store=True, readonly=True),
		'code': fields.integer("Code",size=4),
		'echelon': fields.integer("Echelon",size=2),
		}
rh_fonction_echelon();



