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

from datetime import date, datetime
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


    def _add_months(self, date_, months):
        date_ = datetime.strptime(date_, '%Y-%m-%d')
        month_abs = date_.year * 12 + date_.month + months - 1
        date_ret = date(month_abs // 12, month_abs % 12 + 1, date_.day) 
        return date_ret

    def compute(self, cr, uid, ids, context=None):
        #year = 2014
        unknown = 0
        year = self.browse(cr, uid, ids[0]).year
        target_year = year + 1
        rulepool = self.pool.get('hr.advancement.echelon.rule')
        proposal_pool = self.pool.get('hr.advancement.proposal')
        employee_advancement_pool = self.pool.get('hr.advancement.proposal.employee')
        employee_grade_pool = self.pool.get('hr.employee.grade')
        employee_grade_ids = employee_grade_pool.search(cr, uid, [('state', '=', 'current')])
        employee_grades = employee_grade_pool.browse(cr, uid, employee_grade_ids)
        for employee_grade in list(employee_grades):
            rule_ids = rulepool.search(cr, uid, [('state', '=', 'active'),
                                                ('grade_id', '=', employee_grade.grade_id.id),
                                                ('echelon', '=', employee_grade.echelon),])
            if not rule_ids:
                unknown += 1
                continue
            rule = rulepool.browse(cr, uid, rule_ids[0])
            pace = employee_grade.advancement_pace
            if pace == 'F':
                months = rule.months_fast
            elif pace == 'M':
                months = rule.months_medium
            else:
                months = rule.months
            advancement_date = self._add_months(employee_grade.date_start, months)
            if advancement_date.year < target_year:
                # Get or create advancement proposal
                proposal_ids = proposal_pool.search(cr, uid, [('year', '=', year), ('grade_id', '=', rule.grade_id.id)])
                proposal_id = (proposal_ids and proposal_ids[0] or
                               proposal_pool.create(cr, uid, {'year': year, 'grade_id': rule.grade_id.id}))
                # add employee proposal
                employee_advancement_proposal = {
                    'proposal_id': proposal_id,
                    'employee_id': employee_grade.employee_id.id,
                    'grade_id': employee_grade.grade_id.id,
                    'echelon': employee_grade.echelon + 1,
                    'date_start': advancement_date,  #.strftime('%Y-%m-%d'),
                    'state': 'proposal',
                }
                employee_advancement_pool.create(cr, uid, employee_advancement_proposal)

        _logger.info('%d rules not found!' % (unknown,))

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

