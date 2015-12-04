from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class rh_departement(osv.osv):
	_name = 'rh.departement'
	
	
	_columns = {
		'etablissement_id':fields.many2one("rh.etablissement", "Etablissement"),
		'name': fields.char("Name",size=128),
		'code': fields.char("Code",size=128),
		'logo': fields.binary("Logo du departement"),
		'notes': fields.text('Notes'),
		}
rh_departement()
