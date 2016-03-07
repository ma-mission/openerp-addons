# -*- coding: utf-8 -*-

import time

from openerp.osv import osv, fields
import logging
_logger = logging.getLogger(__name__)

class employee(osv.Model):
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

    def _get_employees(self, cr, uid, ids, context=None):
        res = {}
        for employee_grade in self.browse(cr, uid, ids):  # self is hr.employee.grade
            res[employee_grade.employee_id.id] = True
        return res.keys()

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
                                    relation='hr.grade', string='Grade', readonly=True,
                                    store={_name: (lambda self,cr,uid,ids,c={}: ids, None, 10),
                                           'hr.employee.grade': (_get_employees, None, 10),}),
        'grade_category_id': fields.related('grade_id', 'category_id', type='many2one',
                                            relation='hr.grade.category', string='Grade Category',
                                            readonly=True),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
