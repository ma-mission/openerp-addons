# -*- coding: utf-8 -*-

from tempfile import TemporaryFile
import base64
import csv
import itertools
#import datetime
from datetime import datetime, date, timedelta

import logging
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)


def convert_date(value):
    _logger.info('Converting date %s' % (value,))
    if not value or value[:2] == '  ':
        return None
    date_ = False
    if '/' in value:
        date_ = datetime.strptime(value, '%d/%m/%Y')
    elif value[0:4] == '0000':
        date_ = datetime.strptime(value, '0000%Y')
    elif len(value) == 8:
        date_ = datetime.strptime(value, '%d%m%Y')
    return date_ and datetime.strftime(date_, '%Y-%m-%d') or value

def get_import_messages(result):
    messages = []
    for message in result['messages']:
        message_txt = message['message']
        if message_txt not in messages:
            messages.append(message_txt)
    return messages

class salary_line(osv.osv_memory):
    _name = "hr.salary.wizard.salary.line"
    _description = "Import wizard employee"

    _columns = {
        'wizard_id': fields.many2one('hr.salary.wizard', 'Wizard'),
        'employee_id': fields.many2one('hr.salary.wizard.employee', 'Employee'),
        'employee_number': fields.integer('Employee N'),
        'salary_rule_id': fields.many2one('hr.salary.rule','Rule'),
        'amount': fields.float('Amount', digits=(16,2), required=True),
        #'salary_id': fields.many2one('hr.salary.wizard.salary', 'salary'),
    }

#class employee_salary(osv.osv_memory):
#    _name = "hr.salary.wizard.salary"
#    _inherits = [('hr.salary.wizard.employee','employee_id')]
#    _columns = {
#        'wizard_id': fields.many2one('hr.salary.wizard', 'Wizard', required=True),
#        'employee_id': fields.many2one('hr.salary.wizard.employee', 'Employee'),
#        'line1_ids': fields.one2many('hr.salary.wizard.salary.line', 'salary_id', 'Lines'),
#        'line2_ids': fields.one2many('hr.salary.wizard.salary.line', 'salary_id', 'Lines'),

class employee(osv.osv_memory):
    _name = "hr.salary.wizard.employee"
    _description = "Import wizard employee"

    _columns = {
        'wizard_id': fields.many2one('hr.salary.wizard', 'Wizard', required=True),
        'employee_id': fields.integer('Employee id'),
        'national_id': fields.char('National id', size=10),
        'employee_name': fields.char('Name', size=50),
        'gender': fields.char('Gender', size=2),
        'nationality': fields.char('Nationality', size=2),
        #'birth_date': fields.date('Birth Date'),
        'birth_date': fields.char('Birth Date', size=10),
        #'employment_date': fields.date('Employment Date'),
        'employment_date': fields.char('Employment Date', size=10),
        'chapter_id': fields.many2one('hr.salary.chapter','Chapter'),
        'residence_id': fields.many2one('hr.salary.residence','Residence'),
        'date_start_echelon': fields.char('Echelon start date', size=10),
        'date_start': fields.char('Start date', size=10),
        #'date_start': fields.function(_get_date, type='char', store=True, fnct_inv=_set_date),
        'date_end': fields.char('End date', size=10),
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
        'new': fields.boolean('New employee'),
        'line_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line1_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line2_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line3_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line4_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line5_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line6_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line7_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line8_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line9_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line10_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line11_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line12_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
        'line13_ids': fields.one2many('hr.salary.wizard.salary.line', 'employee_id', 'Lines'),
    }

    _defaults = {
        'new': lambda *a: False,
    }

class salary_import(osv.osv_memory):
    _name = "hr.salary.wizard"
    _description = "Import wizard"

    _columns = {
        'year': fields.integer('Year', readonly=True),
        'month': fields.integer('Month', readonly=True),
        'date': fields.date('Date'),
        'employee_data': fields.binary('Employees', required=True),
        'salary_data': fields.binary('Salaries'),
        'one_liner': fields.boolean('History'),
        'create_new': fields.boolean('Create new employees'),
        'employee_ids': fields.one2many('hr.salary.wizard.employee', 'wizard_id', 'Employees'),
        'employee_messages': fields.text('Messages'),
        'salary_messages': fields.text(),
        #'employee_salary_ids': fields.one2many('hr.salary.wizard.employee.salary', 'wizard_id', 'Employee salaries'),
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

    def create_payslip(self, cr, uid, employee_id, employee, lines, context=None):
        date_start_str = convert_date(employee.date_start)
        date_end_str = convert_date(employee.date_end)
        date_start = datetime.strptime(date_start_str, '%Y-%m-%d')
        date_end = date_end_str and datetime.strptime(date_end_str, '%Y-%m-%d')

        # search for similar grade info
        employee_grade_ids = self.pool.get('hr.employee.grade').search(cr, uid, [
                    ('employee_id', '=', employee_id),
                    ('grade_id', '=', employee.grade_id.id),
                    ('echelon', '=', employee.echelon),
                    ('index', '=', employee.index)])
        if employee_grade_ids:
            # use existing grade info
            employee_grade_id = employee_grade_ids[0] 
        else:
            # create new
            val = {
                    'date_start': convert_date(employee.date_start_echelon or employee.date_start),
                    'employee_id': employee_id,
                    'grade_id': employee.grade_id.id,
                    'echelon': employee.echelon,
                    'index': employee.index,
                    'state': 'confirmed',  # not draft and not necessarily current
            }
            employee_grade_id = self.pool.get('hr.employee.grade').create(cr, uid, val)

        # look for other payslips over crossing period
        payslip_ids = self.pool.get('hr.payslip').search(cr, uid, [
                ('employee_id', '=', employee_id),
                '!', '|', ('date_end', '<=', date_start), ('date_start', '>=', date_end),  # allow one day intersection
            ])

        # overwrite existing payslips
        for payslip in self.pool.get('hr.payslip').browse(cr, uid, payslip_ids):
            _logger.info('Payslip conflict : exist[%s - %s] vs new[%s - %s].' % (payslip.date_start, payslip.date_end, date_start_str, date_end_str))
            if payslip.date_start >= date_start_str and payslip.date_end <= date_end_str:  # old payslip obsoleted, delete
                _logger.info('over the exact same period, delete')
                self.pool.get('hr.payslip').unlink(cr, uid, payslip.id)
            elif payslip.date_start < date_start_str:  # reduce date_end
                _logger.info('reduce date_end')
                self.pool.get('hr.payslip').write(cr, uid, payslip.id, {'date_end': date_start - timedelta(days=1)})
            elif payslip.date_end > date_end_str:  # reduce date_start
                _logger.info('reduce date_start')
                self.pool.get('hr.payslip').write(cr, uid, payslip.id, {'date_start': date_end + timedelta(days=1)})
            #elif payslip.date_end > date_start_str:  # reduce date_end
            #elif payslip.date_start < date_end_str:  # reduce date_start

        extend = False  # just create payslip, do not extend
        #payslip_ids = self.pool.get('hr.payslip').search(cr, uid, [('date_start', '=', date_start), ('employee_id', '=', employee_id)])
        if extend and payslip_ids:
            payslip = self.pool.get('hr.payslip').browse(cr, uid, payslip_ids[0])
            if datetime.strptime(payslip.date_end, '%Y-%m-%d') < date_end:  # extend
                self.pool.get('hr.payslip').write(cr, uid, payslip.id, {'date_end': date_end})
        else:
            # create payslip
            val = {
                    'date_start': date_start,
                    'date_end': date_end,
                    'employee_id': employee_id,
                    'residence_id': employee.residence_id.id,
                    'chapter_id': employee.chapter_id.id,
                    'nationality': employee.nationality,
                    'marital_status': employee.marital_status,
                    'children_number': employee.children_number,
                    'deduction_rate': employee.deduction_rate,
                    'employee_grade_id': employee_grade_id,
            }
            payslip_id = self.pool.get('hr.payslip').create(cr, uid, val)
            # add lines
            for line in lines:
                    if not line.amount:
                        continue
                    val = {
                        #'employee_id': employee_id,
                        'payslip_id': payslip_id,
                        'salary_rule_id': line.salary_rule_id.id,
                        'amount': line.amount,
                    }
                    self.pool.get('hr.payslip.line').create(cr, uid, val)
            # calculate payslip
            def add(x,y): return x+y
            allowances = [line.amount for line in lines if line.salary_rule_id.positive]
            deductions = [line.amount for line in lines if not line.salary_rule_id.positive]
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
            self.pool.get('hr.payslip').write(cr, uid, payslip_id, val)

    def create_payslips(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids[0])
        employees = this.employee_ids
        for employee in employees:
            # find the employee
            employee_ids = self.pool.get('hr.employee').search(cr, uid, [('employee_id', '=', employee.employee_id)])
            if employee_ids: # employee exists
                employee_id = employee_ids[0]
            else:  # this is a new employee, mark and skip
                employee.write({'new': True})
                if not this.create_new:
                    continue
                vals = {
                        'employee_id': employee.employee_id,
                        'identification_id': employee.national_id,
                        'name': employee.employee_name.rstrip(),
                        'gender': employee.gender == 'F' and 'female' or 'male',
                        'birthday': convert_date(employee.birth_date),
                        'public_employment_date': convert_date(employee.employment_date), 
                        'marital_status': employee.marital_status in self._marital_status
                                and self._marital_status[employee.marital_status],
                        'children': employee.children_number,
                        }
                employee_id = self.pool.get('hr.employee').create(cr, uid, vals)
                #continue

            # find salary lines for this employee
            lines = []
            if employee.wizard_id.one_liner:
                lines = employee.line_ids
            else:
                line_ids = self.pool.get('hr.salary.wizard.salary.line').search(cr, uid, [
                        ('wizard_id', '=', ids[0]),
                        ('employee_number', '=', employee.employee_id)])
                lines = self.pool.get('hr.salary.wizard.salary.line').browse(cr, uid, line_ids)
            #_logger.info('Employee %s has %d salary lines.' % (employee.employee_name, len(list(lines))))
            self.create_payslip(cr, uid, employee_id, employee, lines, context)

    _marital_status = {
            'C': 'single',
            'M': 'married',
            'D': 'divorced',
            'V': 'widower',
            }

    _monthly_fields = [
            'employee_id',
            'national_id',
            'employee_name',
            'gender',
            'nationality',
            'birth_date',
            'employment_date',
            'chapter_id',
            'residence_id',
            'date_start_echelon',
            'grade_id',
            'echelle',
            'echelon',
            'index',
            'zone',
            'function',
            'marital_status',
            'children_number',
            'deduction_rate',
        ]

    _history_fields = [
            'chapter_id',
            '',
            'date_start',
            'date_end',
            'employee_id',
            'national_id',
            'employee_name',
            'gender',
            'marital_status',
            'children_number',
            'birth_date',
            'employment_date',
            'nationality',
            'residence_id',
            'zone',
            '',
            '',#'situation',
            'index',
            'grade_id',
            '',
            'echelon',
            '',#space
            '',#brut
            '',#net
            '',
            '',
            '',#nblines
            'line1_ids/salary_rule_id',
            'line1_ids/amount',
            'line2_ids/salary_rule_id',
            'line2_ids/amount',
            'line3_ids/salary_rule_id',
            'line3_ids/amount',
            'line4_ids/salary_rule_id',
            'line4_ids/amount',
            'line5_ids/salary_rule_id',
            'line5_ids/amount',
            'line6_ids/salary_rule_id',
            'line6_ids/amount',
            'line7_ids/salary_rule_id',
            'line7_ids/amount',
            'line8_ids/salary_rule_id',
            'line8_ids/amount',
            'line9_ids/salary_rule_id',
            'line9_ids/amount',
            'line10_ids/salary_rule_id',
            'line10_ids/amount',
            'line11_ids/salary_rule_id',
            'line11_ids/amount',
            'line12_ids/salary_rule_id',
            'line12_ids/amount',
            'line13_ids/salary_rule_id',
            'line13_ids/amount',
        ]
    def import_salaries(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        this = self.browse(cr, uid, ids[0])
        context['default_wizard_id'] = ids[0]

        action={
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'hr.salary.wizard',
            'model': 'hr.salary.wizard',
            'target': 'new',
            'context': context,
            'res_id': ids[0],
            'context': {'form_view_ref': 'hr_payroll_ma.view_hr_salary_import_result'},
        }

        if not this.one_liner:
            # compute end date for monthly payslips
            date_start = datetime.strptime(this.date, '%Y-%m-%d')
            context['default_date_start'] = date(day=1, month=date_start.month, year=date_start.year)
            next_month = date(day=1, month=date_start.month, year=date_start.year) + timedelta(days=31)
            context['default_date_end'] = date(day=1, month=next_month.month, year=next_month.year) - timedelta(days=1)
            import_fields = self._monthly_fields
        else:
            import_fields = self._history_fields

        data = this.employee_data
        _logger.info('Preparing employee information for import.')
        data = data and [list(itertools.compress(row.split('|'),import_fields)) for row in base64.decodestring(data).splitlines() if row != ''] or []
        _logger.info('Importing employee information.')
        import_fields = filter(None, import_fields)
        result = self.pool.get('hr.salary.wizard.employee').load(cr, uid, import_fields, data, context=context)
        employee_messages = get_import_messages(result)
        if employee_messages:
            this.write({'employee_messages': '\n'.join(employee_messages)})
            return action

        if not this.one_liner:
            data = this.salary_data
            _logger.info('Preparing salary information for import.')
            data = data and [row.split('|') for row in base64.decodestring(data).splitlines() if row != ''] or []
            fields = [
                'employee_number',
                'salary_rule_id',
                'amount',
            ]
            _logger.info('Importing salary information.')
            result = self.pool.get('hr.salary.wizard.salary.line').load(cr, uid, fields, data, context=context)
            salary_messages = get_import_messages(result)
            if salary_messages:
                this.write({'salary_messages': '\n'.join(salary_messages)})
                return action

        _logger.info('Creating payslips.')
        self.create_payslips(cr, uid, ids, context=context)
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
