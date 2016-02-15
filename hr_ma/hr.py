# -*- coding: utf-8 -*-

#import logging
from openerp.osv import fields, osv
#from openerp import tools
#_logger = logging.getLogger(__name__)

class employee(osv.osv):
    _name = "hr.employee"
    _inherit = "hr.employee"

    def compute_name(self, cr, uid, ids, givenname, surname, context=None):
        if context is None:
            context = {}
        givenname = givenname or ''
        surname = surname or ''
        fullname = surname.upper() + ' ' + givenname.title()
        return {'value': {'name': fullname}}

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name.isdigit() and operator in ['=', 'ilike']:
            operator = '='
            ids = self.search(cr, uid, [('employee_id', operator, name)] + args, context=context, limit=limit)
        else:
            ids = self.search(cr, uid, [('name', operator, name)] + args, context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)

    def _get_fullname(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context):
            res[employee.id] = ' '.join((
                    employee.givenname or '',
                    employee.surname or ''))
        return res

    _columns = {
        'givenname': fields.char('Given Name', size=40),
        'surname': fields.char('Surname', size=40),
        'fullname': fields.function(
                _get_fullname, type='char', string='Full Name',
                size=80, method=True, readonly=True, store=True),
        'givenname_latin': fields.char('Given Name Lat', size=40),
        'surname_latin': fields.char('Surname Lat', size=40),
        'employee_id': fields.integer('Employee ID', required=True),
        'public_employment_date': fields.date('Employment Date'),
        #'work_start_date': fields.date('Work Start Date'),
        'job_start_date': fields.date('Job Start Date'),
        'birthplace': fields.char('Birth place', size=32),
        'children': fields.integer('Children'),
    }
employee()


class hr_job(osv.osv):
    _inherit = 'hr.job'

    _columns = {
        'name': fields.char('Job Name', size=128, required=True, select=True, translate=True),
    }
hr_job()

