# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class study(osv.osv):
    _name = "hr.study"
    _description = ""

    _columns = {
        'name': fields.char('Study', size=64),
        'employee_id': fields.many2one('hr.employee', 'Employee'),
        'date': fields.date('Date'),
        'paper': fields.binary('Paper'),
    }

study()


class employee(osv.osv):
    _inherit = "hr.employee"

    _columns = {
        'study_ids': fields.one2many('hr.study', 'employee_id', 'Studies'),
    }

employee()

