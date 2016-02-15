# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class EchelonAdvancementRule(osv.Model):
    _name = 'hr.advancement.echelon.rule'
    _description = 'Echelon advancement rule'

    _columns = {
        'ruleset_id': fields.many2one('hr.advancement.ruleset', 'Rule set'),
        'echelon': fields.integer('Echelon'),
        'months': fields.integer('Months'),
        'months_medium': fields.integer('Months Medium'),
        'months_fast': fields.integer('Months Fast'),
    }


class EchelonAdvancementRuleSet(osv.Model):
    _name = 'hr.advancement.ruleset'
    _description = 'Advancement ruleset'

    _columns = {
        'name': fields.char('Name', size=128),
        'date': fields.integer('Effect date'),
        'grade_ids': fields.many2many('hr.grade', 'grade_advancement_rule_rel', 'ruleset_id', 'grade_id', 'Grades'),
        'echelon_rule_ids': fields.one2many('hr.advancement.echelon.rule', 'ruleset_id', 'Echelon rules'),
    }


class EmployeeAdvancementProposal(osv.Model):
    _name = 'hr.advancement.proposal.employee'
    _description = 'Employee advancement proposal'
    _inherits = {'hr.employee.grade': 'employee_grade_id'}

    _columns = {
        #'employee_id': fields.many2one('hr.employee', 'Employee'),
        #'grade_id': fields.many2one('hr.grade', 'Employee'),
        #'echelon': fields.integer('Echelon'),
        #'index': fields.integer('Index'),
        'employee_grade_id': fields.many2one('hr.employee.grade', 'Employee grade', required=True, ondelete='restrict'),
        'proposal_id': fields.many2one('hr.advancement.proposal', 'Advancement Proposal'),
    }


class AdvancementProposal(osv.Model):
    _name = 'hr.advancement.proposal'
    _description = 'Advancement proposal'

    _columns = {
        'year': fields.integer('Year'),
        'grade_id': fields.many2one('hr.grade', 'Grade'),
        'rule_id': fields.many2one('hr.advancement.echelon.rule', 'Rule'),
        'employee_advancement_ids': fields.one2many('hr.advancement.proposal.employee', 'proposal_id', 'Employee Advancements',
                                                    readOnly=True),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

