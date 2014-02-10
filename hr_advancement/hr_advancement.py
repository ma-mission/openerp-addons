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


class EchelonAdvancementRule(osv.osv):
    _name = 'hr.advancement.echelon.rule'
    _description = 'Echelon advancement rule'

    _columns = {
        'ruleset_id': fields.many2one('hr.advancement.ruleset', 'Rule set'),
        'grade_id': fields.many2one('hr.grade', 'Grade'),
        'echelon': fields.integer('Echelon'),
        'months': fields.integer('Months'),
        'months_medium': fields.integer('Months Medium'),
        'months_fast': fields.integer('Months Fast'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('active', 'Active'),
                                   ('superseded', 'Superseded')], 'State'),
    }

    _defaults = {
        'state': 'draft',
    }

    def activate(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'active'})

    def supersede(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'superseded'})

EchelonAdvancementRule()


class AdvancementRuleSet(osv.osv):
    _name = 'hr.advancement.ruleset'
    _description = 'Advancement rule set'

    _columns = {
        'name': fields.char('Name', size=128),
        'reference': fields.char('Reference', size=32),
        'echelon_rule_ids': fields.one2many('hr.advancement.echelon.rule', 'ruleset_id', 'Echelon rules'),
    }

AdvancementRuleSet()


class EmployeeAdvancementProposal(osv.osv):
    _name = 'hr.advancement.proposal.employee'
    _description = 'Employee advancement proposal'
    _inherits = {'hr.employee.grade': 'employee_grade_id'}

    _columns = {
        'proposal_id': fields.many2one('hr.advancement.proposal', 'Advancement Proposal'),
    }

EmployeeAdvancementProposal()


class AdvancementProposal(osv.osv):
    _name = 'hr.advancement.proposal'
    _description = 'Advancement proposal'

    _columns = {
        'year': fields.integer('Year'),
        'grade_id': fields.many2one('hr.grade', 'Grade'),
        'employee_advancement_ids': fields.one2many('hr.advancement.proposal.employee', 'proposal_id', 'Employee Advancements',
                                                    readOnly=True),
    }

AdvancementProposal()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

