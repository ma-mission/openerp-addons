# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import datetime

from openerp.osv import fields, osv
import logging

class evaluation(osv.osv):
    _name = "hr.evaluation"
    _description = ""

    __logger = logging.getLogger('hr_evaluation')

    def _get_sum(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for eval_ in self.browse(cr, uid, ids):
            sum_ = (eval_.work_eval + eval_.productivity_eval +
                    eval_.organization_eval + eval_.conduct_eval +
                    eval_.innovation_eval)
            res[eval_.id] = sum_
        return res
        
    def _get_grade_id(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for eval_ in self.browse(cr, uid, ids):
            res[eval_.id] = eval_.employee_id.current_grade_id.id
        return res
        
    def _get_grade_start(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for eval_ in self.browse(cr, uid, ids):
            employee = eval_.employee_id.id
            self.__logger.info('grade id: %s' % eval_.grade_id.id)
            #self.__logger.info('grade name: %s' % eval_.grade_id.grade_id.name)
            grade = eval_.grade_id.grade_id.id
            grade_ids = self.pool.get('hr.employee.grade').search(
                cr, uid, [('employee_id', '=', employee),
                          ('grade_id', '=', grade)],
                order='echelon')
            grade_start = self.pool.get('hr.employee.grade').browse(cr, uid, grade_ids[0]).date_start
            res[eval_.id] = grade_start
        return res
        
    def _get_mark(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for evaluation in self.browse(cr, uid, ids):
            ev = evaluation.sum
            if ev >= 18:
                mark = 'E'
            elif ev >= 16:
                mark = 'V'
            elif ev >= 14:
                mark = 'G'
            elif ev >= 10:
                mark = 'A'
            else:
                mark = 'W'
            res[evaluation.id] = mark
        return res
        
    _columns = {
        'employee_id': fields.many2one('hr.employee','Employee'),
        'year': fields.integer('Year'),
        'work_eval': fields.integer('Work evaluation'),
        'productivity_eval': fields.integer('Productivity evaluation'),
        'organization_eval': fields.integer('Organization evaluation'),
        'conduct_eval': fields.integer('Conduct evaluation'),
        'innovation_eval': fields.integer('Innovation evaluation'),
        'sum': fields.function(_get_sum, string='Sum', type='integer', readOnly=True, store=True),
        #'grade_id': fields.related('employee_id', 'current_grade_id', string='Grade',
        'grade_id': fields.function(_get_grade_id, string='Grade',
                                    type='many2one', relation='hr.employee.grade', readOnly=True, store=True),
        'grade_start': fields.function(_get_grade_start, string='Grade start', type='date', readOnly=True),  #, store=True),
        'mark': fields.function(_get_mark, string='Mark', type='selection',
                                selection=[('E', 'Excellent'),
                                           ('V', 'Very good'),
                                           ('G', 'Good'),
                                           ('A', 'Average'),
                                           ('W', 'Weak'),], 
                                readOnly=True),
    }

    _defaults = {
        'year': lambda *a: datetime.date.today().year,
        'work_eval': 5,
        'productivity_eval': 5,
        'organization_eval': 3,
        'conduct_eval': 4,
        'innovation_eval': 3,
    }

    def _check_values(self, cr, uid, ids, context=None):
        for eval_ in self.browse(cr, uid, ids):
            if (eval_.work_eval>5 or eval_.productivity_eval>5 or
                eval_.organization_eval>3 or eval_.conduct_eval>4 or
                eval_.innovation_eval>3):
                return False
        return True

    _sql_constraints = [
        ('year_employee_uniq', 'unique(employee_id, year)', 'An employee can have only ONE evaluation per year!'),
    ]

    _constraints = [
        (_check_values, 'Incorrect evaluation value', ['work_eval', 'productivity_eval', 'organization_eval',
                                                       'conduct_eval', 'innovation_eval']),
    ]

evaluation()

class employee_grade(osv.osv):
    _name = "hr.employee.grade"
    _inherit = "hr.employee.grade"

    def _get_avg(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for employee_grade in self.browse(cr, uid, ids):
            year_min = datetime.datetime.strptime(employee_grade.date_start, '%Y-%m-%d').year
            year_max = employee_grade.date_end and datetime.datetime.strptime(employee_grade.date_end, '%Y-%m-%d').year
            conds = [('employee_id','=',employee_grade.employee_id.id), ('year','>=',year_min)]
            if year_max:
                conds.append(('year','<=',year_max))
            eval_ids = self.pool.get('hr.evaluation').search(cr, uid, conds)
            evals = self.pool.get('hr.evaluation').browse(cr, uid, eval_ids)
            sum_ = sum([eval_.sum for eval_ in evals])
            avg = len(evals) and float(sum_) / len(evals)
            res[employee_grade.id] = avg
        return res

    def _get_pace(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for employee_grade in self.browse(cr, uid, ids):
            avg = employee_grade.evaluation_avg
            if avg >= 16:
                pace = 'F'
            elif avg >= 10:
                pace = 'M'
            else:
                pace = 'S'
            res[employee_grade.id] = pace
        return res
        
    def _get_employee_grade_from_evaluation(self, cr, uid, ids, context={}):
        res = set()
        for evaluation in self.pool['hr.evaluation'].browse(cr, uid, ids, context=context):
            date = datetime.datetime(evaluation.year+1, 1, 1)
            employee_grade_ids = self.pool['hr.employee.grade'].search(cr, uid, [('date_start', '<', date)], context=context)
            res.update(employee_grade_ids)
        return res

    _columns = {
        'evaluation_avg': fields.function(_get_avg, string='Evaluation average', type='float'),
        'advancement_pace': fields.function(_get_pace, string='Advancement pace', type='selection',
                                selection=[('F', 'Fast'),
                                           ('M', 'Medium'),
                                           ('S', 'Slow'),], 
                                store={_name: (lambda self,cr,uid,ids,c={}: ids, None, 10),
                                    'hr.evaluation': (_get_employee_grade_from_evaluation, None, 10),},
                                readOnly=True),
    }

employee_grade()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
