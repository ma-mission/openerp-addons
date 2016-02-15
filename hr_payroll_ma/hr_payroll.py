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
import time

from openerp.osv import fields, osv

class salary_rule(osv.osv):
    _name = "hr.salary.rule"
    _description = "Salary rule"

    _columns = {
        'ref': fields.integer('Reference', select=True),
        'name': fields.char('Name', size=30, select=True),
        'positive': fields.boolean('Positive'),
    }

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name.isdigit():
            ids = self.search(cr, uid, [('ref', operator, name)] + args, context=context, limit=limit)
        else:
            ids = self.search(cr, uid, [('name', operator, name)] + args, context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)

salary_rule()

class salary_residence(osv.osv):
    _name = "hr.salary.residence"
    _description = "Residence"
    _rec_name = "ref"

    _columns = {
        'ref': fields.integer('Reference', select=True),
        'name': fields.char('Name', size=30, select=True),
    }
salary_residence()

class salary_chapter(osv.osv):
    _name = "hr.salary.chapter"
    _description = "Residence chapter"
    _rec_name = "ref"

    _columns = {
        'ref': fields.integer('Reference', select=True),
        'name': fields.char('Name', size=50, select=True),
    }
salary_chapter()

class payslip_line(osv.osv):
    _name = "hr.payslip.line"
    _description = "Payslip Line"

    _columns = {
        'salary_rule_id': fields.many2one('hr.salary.rule','Rule'),
        'payslip_id': fields.many2one('hr.payslip','Payslip'),
        'amount': fields.float('Amount', digits=(16,2), required=True),
    }
payslip_line()

class payslip(osv.osv):
    _name = "hr.payslip"
    _description = "Payslip"

    _columns = {
        'employee_id': fields.many2one('hr.employee','Employee'),
        'employee_grade_id': fields.many2one('hr.employee.grade','Employee Grade', ondelete='restrict'),
        'line_ids': fields.one2many('hr.payslip.line', 'payslip_id', 'Lines'),
        'date_start': fields.date('Start Date'),
        'date_end': fields.date('End date'),
        'residence_id': fields.many2one('hr.salary.residence','Residence'),
        'chapter_id': fields.many2one('hr.salary.chapter','Chapter'),
        'marital_status': fields.selection((('C', 'Celibataire'), ('M', 'Marie'), ('D', 'Divorce'), ('V', 'Veuf'), ('J', 'Autre')), 'Marital Status'),
        'children_number': fields.integer('# Children'),
        'deduction_rate': fields.integer('Deduction Rate'),
        'total_allowances': fields.float('Gross'),
        'total_deductions': fields.float('Deductions'),
        'net_annual': fields.float('Net'),
        'net_monthly': fields.float('Monthly'),
        'nationality': fields.char('Nationality', size=2),  # should not change but uses non standard codes
        #'_id': fields.many2one('hr.',''),
    }

    _defaults = {
        'date_start': lambda *a: time.strftime("%Y-%m-01"),
    }
payslip()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
