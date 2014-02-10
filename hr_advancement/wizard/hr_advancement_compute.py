# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 me!
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

from openerp.osv import fields, osv

from datetime import date
import logging


_logger = logging.getLogger('adv_wiz')

class advancementWizard(osv.osv_memory):
    _name = 'hr.advancement.wizard'
    _description = 'Advancement wizard'

    _columns = {
        'year': fields.integer('Year'),
    }

    _defaults = {
        'year': 2013,  # lambda a: date.today().year
    }

    def _get_employee_grades(self, cr, uid, grade_id, echelon, pace, year, months):
        _logger.info('Rule : %s, %s, %s, %d' % (grade_id, echelon, pace, months))
        sql = "select id from hr_employee_grade where grade_id=%d and echelon=%d and date_start<%s"
        month_ref = year * 12 + 12 - months
        date_ref = date(month_ref // 12, month_ref % 12 + 1, 1) 
        _logger.info(' -> Date : %s' % (date_ref,))
        employee_grade_ids = self.pool.get('hr.employee.grade').search(
            cr, uid, [('grade_id', '=', grade_id.id),
                      ('echelon', '=', echelon),
                      ('advancement_pace', '=', pace),
                      ('date_start', '<', date_ref),
                      ])
        _logger.info('Employee_grades: %s' % (employee_grade_ids))
        return employee_grade_ids or []

    def compute(self, cr, uid, ids, context=None):
        #year = 2014
        year = self.browse(cr, uid, ids[0]).year
        target_year = year + 1
        rulepool = self.pool.get('hr.advancement.echelon.rule')
        proposal_pool = self.pool.get('hr.advancement.proposal')
        employee_advancement_pool = self.pool.get('hr.advancement.proposal.employee')
        rule_ids = rulepool.search(cr, uid, [('state', '=', 'active')])
        rules = rulepool.browse(cr, uid, rule_ids)
        for rule in rules:
            _logger.info('# Rule %d: %s' % (rule.id, rule.grade_id,))

            slow = self._get_employee_grades(cr, uid, rule.grade_id, rule.echelon, 'S', target_year, rule.months)
            medium = self._get_employee_grades(cr, uid, rule.grade_id, rule.echelon, 'M', target_year, rule.months_medium)
            fast = self._get_employee_grades(cr, uid, rule.grade_id, rule.echelon, 'F', target_year, rule.months_fast)
            employee_grade_ids = slow + medium + fast

            _logger.info('Employee_grades_all: %s' % (employee_grade_ids))
            employees = [self.pool.get('hr.employee.grade').browse(cr, uid, eg).employee_id.name for eg in employee_grade_ids]
            _logger.info('Employees: %s' % (employees,))

            if employee_grade_ids:
                # Get or create advancement proposal
                proposal_ids = proposal_pool.search(cr, uid, [('year', '=', year), ('grade_id', '=', rule.grade_id.id)])
                proposal_id = (proposal_ids and proposal_ids[0] or
                               proposal_pool.create(cr, uid, {'year': year, 'grade_id': rule.grade_id.id}))
                # add employee proposal
                for employee_grade_id in employee_grade_ids:
                    employee_advancement_pool.create(cr, uid, {'proposal_id': proposal_id,
                                                               'employee_grade_id': employee_grade_id})

        action={
            'string': 'Advancement proposals',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'hr.advancement.proposal',
            'model': 'hr.advancement.proposal',
            #'target': 'new',
            'context': context,
            'domain': [('year', '=', year)],
        }
        return action

advancementWizard()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

