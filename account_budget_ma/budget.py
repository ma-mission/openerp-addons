# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
#import logging
#_logger = logging.getLogger(__name__)

class budget(osv.osv):
    _name = 'account.budget'

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'line_ids': fields.one2many('account.budget.line', 'budget_id', 'Budget lines'),
    }


class budget_line(osv.osv):
    _name = 'account.budget.line'

    def _committed_amount(self, cr, uid, ids, name, args, context=None):
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            cr.execute("SELECT SUM(amount) FROM account_analytic_line "
                    "WHERE general_account_id=%s AND account_id=%s "
                    "AND date BETWEEN to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')",
                    (line.general_account_id.id, line.analytic_axis_id.id,
                    line.budget_id.fiscalyear_id.date_start, line.budget_id.fiscalyear_id.date_stop))
            result = cr.fetchone()[0]
            if result is None:
                result = 0.00
            res[line.id] = result
        return res

    def _get_budget_line_from_commitment(self, cr, uid, ids, context={}):
        res = set()
        for commitment in self.pool['account.analytic.line'].browse(cr, uid, ids, context=context):
            budget_ids = self.pool['account.budget'].search(cr, uid, 
                    [('company_id', '=', commitment.company_id.id),
                    ('fiscalyear_id', '=', self.pool['account.fiscalyear'].find(cr, uid, commitment.date, context=context))])
            line_ids = self.pool['account.budget.line'].search(cr, uid, 
                    [('general_account_id', '=', commitment.general_account_id.id),
                    ('analytic_axis_id', '=', commitment.account_id.id),
                    ('budget_id', 'in', budget_ids)])
            res.update(line_ids)
        return res


    _columns = {
        'budget_id': fields.many2one('account.budget', 'Budget', required=True),
        'general_account_id': fields.many2one('account.account', 'General account', required=True),
        'analytic_axis_id': fields.many2one('account.analytic.account', 'Analytic Axis', required=True),
        'amount': fields.float('Amount', digits_compute=dp.get_precision('Account'), required=True),
        'committed_amount': fields.function(_committed_amount, string='Committed', type='float', digits_compute=dp.get_precision('Account'),
            store={'account.analytic.line': (_get_budget_line_from_commitment, None, 10)}),
    }

