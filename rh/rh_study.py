from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class rh_study(osv.osv):
	_name = 'rh.study'
	

		
	_columns = {
		'employe_id': fields.many2one("rh.employe","Employe"),
		'qualification_id': fields.many2one("rh.qualification",string="Qualification"),
		'date': fields.date("Date of graduation"),
		'et_type_id': fields.many2one("rh.et_type","Type etablissement"),
		'et_type_id': fields.many2one("rh.et_type","Type etablissement"),
		'ville_id': fields.many2one("rh.ville","Ville"),
		'support': fields.binary("Support"),
		
			}
rh_study()
