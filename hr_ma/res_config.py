# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class hr_config_settings(osv.osv_memory):
    _inherit = 'hr.config.settings'

    _columns = {
        'module_hr_mission': fields.boolean('Manage employees missions',
            help ="""This installs the module hr_mission."""),
        'module_hr_evaluation_ma': fields.boolean('Manage employees evaluations',
            help ="""This installs the module hr_evaluation_ma."""),
        'module_hr_advancement': fields.boolean('Manage employees advanacements',
            help ="""This installs the module hr_mission."""),
        'module_hr_payroll_ma': fields.boolean('Manage payslips',
            help ="""This installs the module hr_payroll_ma."""),
    }

    def onchange_hr_advancement(self, cr, uid, ids, advancement, context=None):
        """ module_hr_advancement implies module_hr_evalution_ma """
        if advancement:
            return {'value': {'module_hr_evaluation_ma': True}}
        return {}

    def onchange_hr_evaluation_ma(self, cr, uid, ids, evaluation_ma, context=None):
        """ module_hr_advancement implies module_hr_evalution_ma """
        if not evaluation_ma:
            return {'value': {'module_hr_advancement': False}}
        return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
