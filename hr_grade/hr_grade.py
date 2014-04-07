# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2014 Université Hassan 1er.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from osv import fields, osv

class grade(osv.osv):
    _name = "hr.grade"
    _description = ""

    _columns = {
        'name': fields.char('Name', size=50, translate=True),
        'ref': fields.integer('Reference', select=True),
    }

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name.isdigit():
            ids = self.search(cr, uid, [('ref', operator, name)] + args, context=context, limit=limit)
        else:
            ids = self.search(cr, uid, [('name', operator, name)] + args, context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)

    _sql_constraints = [
        ('ref_uniq', 'unique(ref)', 'The reference of the grade must be unique'),
    ]

grade()


class employee_grade(osv.osv):
    _name = "hr.employee.grade"
    _description = ""

    _columns = {
        'employee_id': fields.many2one('hr.employee','Employee'),
        'grade_id': fields.many2one('hr.grade','Grade'),
        #'grade_ref': fields.related('grade_id','ref', type='integer', relation='hr.grade', string='Grade Reference',  store=False),
        #'echelle': fields.integer(''),
        'echelon': fields.integer('Echelon'),
        'index': fields.integer('Index'),
        'date_start': fields.date('Start date'),
        'date_end': fields.date('End date'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('proposal', 'Proposal'),
                                   ('current', 'Current'),
                                   ('old', 'Old')], 'State'),
    }

    _defaults = {
        'state': 'draft',
        'date_start': lambda *a: time.strftime("%Y-%m-01"), # first day of month
    }

employee_grade()


class employee(osv.osv):
    _inherit = "hr.employee"
    _name = "hr.employee"

    def _get_cur_grade_id(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for id in ids:
            cur_grade_ids = self.pool.get('hr.employee.grade').search(
                    cr, uid, [('employee_id', '=', id),
                              ('state', '=', 'current')],
                    limit=1, order='date_start desc')
            res[id] = cur_grade_ids and cur_grade_ids[0] or None
        return res

    _columns = {
        'employee_grade_ids': fields.one2many('hr.employee.grade', 'employee_id', 'Employee Grades'),
        'current_grade_id': fields.function(
            _get_cur_grade_id,
            type='many2one',
            obj="hr.employee.grade",
            method=True,
            readonly=True,
            string='Employee Grade'),
        'grade_id': fields.related('current_grade_id', 'grade_id', type='many2one',
                                    relation='hr.grade', string='Grade', readonly=True, store=True),
    }

employee()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
