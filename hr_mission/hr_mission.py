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

from osv import fields, osv

class mission(osv.osv):
    _name = "hr.mission"
    _description = ""

    _track = {
        'state': {
            'hr_mission.mt_mission_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'validate',
            'hr_mission.mt_mission_refused': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'refuse',
        },
    }

    _columns = {
        'employee_id': fields.many2one('hr.employee','Employee'),
        'object': fields.char('Object', size=80),
        #'transport_id': fields.many2one('hr.employee','Transport'),
        'transport': fields.char('Transport', size=50),
        'date_start': fields.date('Depart Date'),
        'date_end': fields.date('Return Date'),
        #'international': fields.boolean('International'),
        #'country_id': fields.many2one('res.country', 'Country'),
        #'city': fields.char('City', size=30),
        'city_from': fields.many2one('res.city', 'Departure'),
        'city_to': fields.many2one('res.city', 'Destination'),
        'transport': fields.selection([('train', 'Train'),
                                       ('car', 'Car'),
                                       ('plane', 'Plane')], 'Transport'),
        'driver_id': fields.many2one('hr.employee', 'Driver', domain=[('job_id','=','Driver')]),
        #'': fields.many2one('.',''),
        'state': fields.selection([('draft', 'Draft'), ('refuse', 'Refused'), ('validate', 'Approved')], 'Status', readonly=True, track_visibility='onchange'),
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
