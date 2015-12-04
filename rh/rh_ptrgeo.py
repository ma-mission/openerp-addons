from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _


class rh_ptrgeo(osv.osv):

	_name = 'rh.ptrgeo'
	_columns = {
        'name': fields.char('Patrimoin Actif'),
					}
rh_ptrgeo()
