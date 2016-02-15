# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class mission(osv.Model):
    _name = "hr.mission"
    _description = ""

    _track = {
        'state': {
            'hr_mission.mt_mission_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'validate',
            'hr_mission.mt_mission_refused': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'refuse',
        },
    }

    _TRANSPORTS = [
            ('train', 'Train'),
            ('fleet', 'Company car'),
            ('personal', 'Personal car'),
            ('plane', 'Plane')
    ]

    def get_transport(self, cr, uid, ids, transport, context=None):  # For reports
        lang = context and 'lang' in context and context['lang']
        for mean in self._TRANSPORTS:
            if mean[0] == transport:
                name = mean[1]
                return self.pool.get('ir.translation')._get_source(cr, uid, None, 'selection', lang, name)

    _columns = {
        #'employee_id': fields.many2one('hr.employee','Employee'),
        'employee_ids': fields.many2many('hr.employee', 'hr_mission_employees', 'mission_id', 'employee_id', 'Employees', readonly=True, states={'draft':[('readonly',False)]}),
        'object': fields.char('Object', size=80, readonly=True, states={'draft':[('readonly',False)]}),
        'date_start': fields.date('Depart Date', readonly=True, states={'draft':[('readonly',False)]}),
        'date_end': fields.date('Return Date', readonly=True, states={'draft':[('readonly',False)]}),
        #'international': fields.boolean('International'),
        #'country_to': fields.many2one('res.country', 'Country'),
        'city_from': fields.many2one('res.city', 'Departure', readonly=True, states={'draft':[('readonly',False)]}),
        'city_to': fields.many2one('res.city', 'Destination', readonly=True, states={'draft':[('readonly',False)]}),
        'transport': fields.selection(_TRANSPORTS, 'Transport', readonly=True, states={'draft':[('readonly',False)]}),
        'driver_id': fields.many2one('hr.employee', 'Driver', domain=[('job_id','=','Driver')], readonly=True, states={'draft':[('readonly',False)]}),
        'car_immatriculation': fields.char('Immatriculation', size=32, readonly=True, states={'draft':[('readonly',False)]}),
        'horsepower': fields.integer('Horsepower', readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection([('draft', 'Draft'), ('validate', 'Approved'), ('refuse', 'Refused')], 'Status', readonly=True, track_visibility='onchange'),
    }

    _defaults = {
        'state': 'draft',
    }

    def mission_validate(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'validate'})

    def mission_refuse(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'refuse'})

    def mission_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'})

    _constraints = [
    ]

    _sql_constraints = [
        ('date_check', "CHECK ( (date_start <= date_end))", "The start date must be anterior to the end date."),
    ]

mission()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
