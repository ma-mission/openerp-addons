from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _


class rh_employe(osv.osv):

	_inherit = 'rh.employe'
	_columns = {
        'ptractif_ids': fields.one2many('ptr.patrimoineactif','responsable',string='Patrimoin Actif'),
					}
rh_employe()
