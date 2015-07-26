from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class rh_doc(osv.osv):
	_name = 'rh.doc'
	_columns = {
		'employee_id': fields.many2one("rh.employee","Employee"),
		'name': fields.char("Name"),
		'date': fields.date("Date of Edit"),
		'date': fields.date("Date"),
		'state':fields.boolean("State"),
		'reason': fields.char("Reason"),
		'adress': fields.text("Adress"),
		'start_date': fields.date("Start date"),
		'end_date': fields.date("End date"),
		
			}
rh_doc()
