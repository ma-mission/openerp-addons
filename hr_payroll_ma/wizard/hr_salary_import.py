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
from tempfile import TemporaryFile
import base64
import csv
#import datetime
from datetime import datetime, date, timedelta

import logging
from osv import fields, osv

_logger = logging.getLogger(__name__)

class salary_lines(osv.osv_memory):
    _name = "hr.salary.wizard.salary.line"
    _description = "Import wizard employee"

    _columns = {
        'wizard_id': fields.many2one('hr.salary.wizard', 'Wizard'),
        'employee_id': fields.many2one('hr.salary.wizard.employee', 'Employee'),
        #'employee_id': fields.integer('Employee'),
        'salary_rule_id': fields.many2one('hr.salary.rule','Rule'),
        'amount': fields.float('Amount', digits=(16,2), required=True),
    }
salary_lines()

class employee(osv.osv_memory):
    _name = "hr.salary.wizard.employee"
    _description = "Import wizard employee"
    #_rec_name = "employee_id"

    _columns = {
        'wizard_id': fields.many2one('hr.salary.wizard', 'Wizard'),
        'employee_id': fields.integer('Employee id'),
        'national_id': fields.char('National id', size=10),
        'employee_name': fields.char('Name', size=50),
        'gender': fields.char('Gender', size=2),
        'nationality': fields.char('Nationality', size=2),
        #'birth_date': fields.date('Birth Date'),
        'birth_date': fields.char('Birth Date', size=8),
        #'employment_date': fields.date('Employment Date'),
        'employment_date': fields.char('Employment Date', size=10),
        'chapter_id': fields.many2one('hr.salary.chapter','Chapter'),
        'residence_id': fields.many2one('hr.salary.residence','Residence'),
        #'date_start': fields.date('Date'),
        'date_start': fields.char('Date', size=10),
        'grade_id': fields.many2one('hr.grade','Grade'),
        'echelle': fields.char('Echelle', size=2),
        'echelon': fields.integer('Echelon'),
        'index': fields.integer('Index'),
        'zone': fields.char('Zone', size=1),
        'function': fields.char('Function', size=8),
        #'marital_status': fields.char('Marital Status', size=1),
        'marital_status': fields.selection((('C', 'Celibataire'), ('M', 'Marie'), ('D', 'Divorce'), ('V', 'Veuf'), ('J', 'Autre')), 'Marital Status'),
        'children_number': fields.integer('# Children'),
        'deduction_rate': fields.integer('Deduction Rate'),
        'line_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
    }

    _defaults = {
        #'date_start': lambda *a: time.strftime("%Y-%m-01"),
    }

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        parts = name.split(',')
        wizard = parts[0]
        employee = parts[1]
        _logger.info('name_search parts .. %s' % repr(parts))
        ids = self.search(cr, uid, [('wizard_id.id', '=', wizard), ('employee_id', '=', employee)], context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)
        #result = [(id, '') for id in ids]
        #_logger.info('name_search result .. %s' % repr(result))
        #return result
        return []
employee()

class salary_import(osv.osv_memory):
    _name = "hr.salary.wizard"
    _description = "Import wizard"

    _columns = {
        'year': fields.integer('Year', readonly=True),
        'month': fields.integer('Month', readonly=True),
        'date': fields.date('Date', readonly=True),
        'employee_data': fields.binary('Employees'),
        'salary_data': fields.binary('Salaries'),
        'employee_ids': fields.one2many('hr.salary.wizard.employee', 'wizard_id', 'Employees'),
        #'line_ids': fields.one2many('hr.salary.wizard.salary.line', 'wizard_id', 'Salary lines')

    }

    def _last_month(*args):
        today = date.today()
        first = date(day=1, month=today.month, year=today.year)
        lastMonth = first - timedelta(days=1)
        lastMonth_first = date(day=1, month=lastMonth.month, year=lastMonth.year)
        return date.strftime(lastMonth_first, '%Y-%m-%d')

    _defaults = {
        #'year': lambda *a: datetime.now().year,
        #'month': lambda *a: datetime.now().month,
        'date': _last_month,
    }

    def create_payslips(self, cr, uid, ids, context=None):
        employees = self.browse(cr, uid, ids[0]).employee_ids
        _logger.info('creating .. %s' % repr(employees))
        for employee in employees: #self.pool.get('hr.salary.wizard.employee').browse(cr, uid, employee_ids):
            date_start = datetime.strptime(employee.date_start, '%d/%m/%Y')
            wiz_date = datetime.strptime(employee.wizard_id.date, '%Y-%m-%d')
            info_date_end = wiz_date - timedelta(days=1)
            nextMonth = wiz_date + timedelta(days=32)
            date_end = datetime(day=1, month=nextMonth.month, year=nextMonth.year) - timedelta(days=1)
            _logger.info('dates .. %s %s %s %s ' % (repr(date_start), repr(info_date_end), repr(wiz_date), repr(date_end)))
            employee_ids = self.pool.get('hr.employee').search(cr, uid, [('employee_id', '=', employee.employee_id)])
            _logger.info('employee_ids .. %s' % repr(employee_ids))
            # update employee info
            val = {
                'employee_id': employee.employee_id,
                'identification_id': employee.national_id,
                'name': employee.employee_name.rstrip(),
                'gender': employee.gender == 'F' and 'female' or 'male',
                #'country_id': employee.nationality,
                'birthday': (employee.birth_date[0:4] == '0000') and datetime.strptime(employee.birth_date, '0000%Y')
                             or datetime.strptime(employee.birth_date, '%d%m%Y'),
                'public_employment_date': datetime.strptime(employee.employment_date, '%d/%m/%Y'),
            }
            if employee_ids: # employee exists: update
                employee_id = employee_ids[0]
                self.pool.get('hr.employee').write(cr, uid, employee_id, val),
                _logger.info('updated user .. %s' % repr(val))
            else: # next
                continue
            # import grade info
            #current_grade_ids = self.pool.get('hr.employee.grade').search(cr, uid, [('employee_id', '=', employee_id),
            #                                                                        #('date_end', '<', employee.wizard_id.date),
            #                                                                        ('date_end', '=', info_date_end)],
            #                                                              limit=1, order='date_start desc')
            #_logger.info('create - current grade .. %s' % repr(current_grade_ids))
            #cgrade = self.pool.get('hr.employee.grade').browse(cr, uid, current_grade_ids)
            #cgrade = cgrade and cgrade[0]
            cgrade = self.pool.get('hr.employee').browse(cr,uid, employee_id).current_grade_id
            # extend old
            if (cgrade and ((cgrade.grade_id.id, cgrade.echelon, cgrade.index) !=
                          (employee.grade_id.id, employee.echelon, employee.index))
                and cgrade.date_end < employee.date_end):
                self.pool.get('hr.employee.grade').write(cr, uid, cgrade.id, {'date_end': date_end})
            # create new
            if not(cgrade and (cgrade.grade_id.id, cgrade.echelon, cgrade.index) ==
                   (employee.grade_id.id, employee.echelon, employee.index)):
                val = {
                    'date_start': date_start,
                    'date_end': date_end,
                    'employee_id': employee_id,
                    'grade_id': employee.grade_id.id,
                    'echelon': employee.echelon,
                    'index': employee.index,
                }
                _logger.info('create employee grade val .. %s' % repr(val))
                grade = self.pool.get('hr.employee.grade').create(cr, uid, val)

            payslip_id = self.pool.get('hr.payslip').search(cr, uid, [('date_start', '=', date_start),
                                                                  #('date_end', '=', info_date_end),
                                                                  ('employee_id', '=', employee_id)])
            _logger.info('create - cheking .. %s' % repr(payslip_id))
            if payslip_id:
                payslip = self.pool.get('hr.payslip').browse(cr, uid, payslip_id)
                if payslip.date_end < date_end:  # extend
                    self.pool.get('hr.payslip').write(cr, uid, payslip_id, {'date_end': date_end})
            else:
                # create payslip
                val = {
                    'date_start': date_start,
                    'date_end': date_end,
                    'employee_id': employee_id,
                    'residence_id': employee.residence_id.id,
                    'chapter_id': employee.chapter_id.id,
                    'marital_status': employee.marital_status,
                    'children_number': employee.children_number,
                    'deduction_rate': employee.deduction_rate,
                }
                _logger.info('create val .. %s' % repr(val))
                payslip_id = self.pool.get('hr.payslip').create(cr, uid, val)
                # add lines
                for line in employee.line_ids:
                    val = {
                        'employee_id': employee_id,
                        'payslip_id': payslip_id,
                        'salary_rule_id': line.salary_rule_id.id,
                        'amount': line.amount,
                    }
                    _logger.info('create val .. %s' % repr(val))
                    self.pool.get('hr.payslip.line').create(cr, uid, val)
                # calculate payslip
                def add(x,y): return x+y
                allowances = [line.amount for line in employee.line_ids if line.salary_rule_id.positive]
                deductions = [line.amount for line in employee.line_ids if not line.salary_rule_id.positive]
                allowance = allowances and reduce(add, allowances) or 0
                deduction = deductions and reduce(add, deductions) or 0
                annual = allowance - deduction
                monthly = annual / 12
                val = {
                    'total_allowances': allowance,
                    'total_deductions': deduction,
                    'net_annual': annual,
                    'net_monthly': monthly,
                }
                _logger.info('create val .. %s' % repr(val))
                self.pool.get('hr.payslip').write(cr, uid, payslip_id, val)

    def import_salaries(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        this = self.browse(cr, uid, ids[0])
        #fileobj = TemporaryFile('w+')
        #try:
            #fileobj.write(base64.decodestring(this.data))
            #csvdata = csv.reader(fileobj, delimiter='|') #, quotechar='|')
        #finally:
            #fileobj.close()
        me = str(ids[0])
        #data = [ row.split('|') for row in base64.decodestring(this.data).split('\n')]
        #_logger.info('importing.. %s' % repr(data))
        data = this.employee_data
        data = data and [(row+me).split('|') for row in base64.decodestring(data).split('\n') if row != ''] or []
        _logger.info('importing.. %s' % repr(data))
        fields = [
            'employee_id',
            'national_id',
            'employee_name',
            'gender',
            'nationality',
            'birth_date',
            'employment_date',
            'chapter_id',
            'residence_id',
            'date_start',
            'grade_id',
            'echelle',
            'echelon',
            'index',
            'zone',
            'function',
            'marital_status',
            'children_number',
            'deduction_rate',
            'wizard_id/.id'
        ]
        result = self.pool.get('hr.salary.wizard.employee').load(cr, uid, fields, data)
        _logger.info('imported.. %s' % repr(result))

        data = this.salary_data
        me = me + ','
        data = data and [(me+row).split('|') for row in base64.decodestring(data).split('\n') if row != ''] or []
        _logger.info('importing.. %s' % repr(data))
        fields = [
            'employee_id',
            'salary_rule_id',
            'amount',
            #'wizard_id/.id'
        ]
        result = self.pool.get('hr.salary.wizard.salary.line').load(cr, uid, fields, data)
        _logger.info('imported.. %s' % repr(result))

        self.create_payslips(cr, uid, ids, context)
        #if result['ids'] == False:
        #    return result

        action={
            'type': 'ir.actions.act_window',
            #'name': 'action_hr_salary_import_employee',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'hr.salary.wizard.employee',
            'model': 'hr.salary.wizard.employee',
            'target': 'new',
            'context': context,
            'domain': [('wizard_id', '=', ids[0])]
        }
        return action

salary_import()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
