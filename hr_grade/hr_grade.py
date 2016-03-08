# -*- coding: utf-8 -*-

import time

from openerp.osv import osv, fields


class grade_category(osv.Model):
    _name = "hr.grade.category"

    _columns = {
        'name': fields.char('Name', size=128),
        'ref': fields.integer('Reference', select=True),
    }

class grade(osv.Model):
    _name = "hr.grade"
    _description = ""

    _columns = {
        'name': fields.char('Name', size=50, translate=True),
        'ref': fields.integer('Reference', select=True),
        'paygrade_id': fields.many2one('hr.paygrade', 'Paygrade'),
        'category_id': fields.many2one('hr.grade.category', 'Category'),
        'echelon_offset': fields.integer('Echelon offset'),
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


class paygrade(osv.Model):
    _name = "hr.paygrade"

    _columns = {
        'name': fields.char('Name', size=16),
        'sequence': fields.integer('Sequence'),
        'echelon_ids': fields.one2many('hr.paygrade.echelon', 'paygrade_id', 'Echelons'),
    }

class paygrade_echelon(osv.Model):
    _name = "hr.paygrade.echelon"

    _columns = {
        'name': fields.char('Name', size=16),
        'paygrade_id': fields.many2one('hr.paygrade', 'Paygrade'),
        'sequence': fields.integer('Sequence'),
        'index': fields.integer('Index'),
    }


class employee_grade(osv.Model):
    _name = "hr.employee.grade"
    _description = ""
    _order = "date_start desc"

    _columns = {
        'employee_id': fields.many2one('hr.employee','Employee'),
        'grade_id': fields.many2one('hr.grade','Grade'),
        'echelon': fields.integer('Echelon'),
        'index': fields.integer('Index'),
        'date_start': fields.date('Start date'),
        'date_end': fields.date('End date'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('confirmed', 'Confirmed'),
                                   ('proposal', 'Proposal'),
                                   ('current', 'Current'),
                                   ('old', 'Old')], 'State'),
    }

    _defaults = {
        'state': 'draft',
        'date_start': lambda *a: time.strftime("%Y-%m-01"), # first day of month
    }

    def grade_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'confirmed'})

    def grade_validate(self, cr, uid, ids, context=None):
        employee_grades = self.browse(cr, uid, ids)
        # Only one employee_grade is current: deprecate current grades first
        for employee_grade in employee_grades:
            current_grade = employee_grade.employee_id.current_grade_id
            if current_grade:
                current_grade.grade_deprecate()
        return self.write(cr, uid, ids, {'state':'current'})

    def grade_deprecate(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'old'})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
