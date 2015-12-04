from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class rh_etablissement(osv.osv):
	_name = 'rh.etablissement'
	
	
	_columns = {
		'name': fields.char("Name",size=128),
		'code': fields.char("Code",size=128),
		'logo': fields.binary("Logo de l\'etablissement"),
		'notes': fields.text('Notes'),
		}
rh_etablissement()
