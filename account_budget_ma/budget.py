# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
#import logging
#_logger = logging.getLogger(__name__)

class budget(osv.osv):
    _name = 'account.budget'

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'period': fields.many2one('account.period', 'Period', required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'line_ids': fields.one2many('account.budget.line', 'budget_id', 'Budget lines'),
    }


class budget_line(osv.osv):
    _name = 'account.budget.line'

    _columns = {
        'budget_id': fields.many2one('account.budget', 'Budget', required=True),
        'general_account_id': fields.many2one('account.account', 'General account', required=True),
        'analytic_axis_id': fields.many2one('account.analytic.account', 'Analytic Axis', required=True),
        'amount': fields.float('Amount', digits_compute=dp.get_precision('Account'), required=True),
    }

