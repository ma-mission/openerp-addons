# -*- coding: utf-8 -*-

import time

from openerp.osv import osv, fields


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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
