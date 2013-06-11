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

#from openerp import addons
#import logging
#from openerp.osv import fields, osv
from osv import fields, osv
#from openerp import tools
#_logger = logging.getLogger(__name__)

class employee(osv.osv):
    _name = "hr.employee"
    _inherit = "hr.employee"

    def compute_name(self, cr, uid, ids, givenname, surname, context=None):
        if context is None:
            context = {}
        givenname = givenname or ''
        surname = surname or ''
        return {'value': {'name': givenname + ' ' + surname}}

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name.isdigit() and operator in ['=', 'ilike']:
            operator = '='
            ids = self.search(cr, uid, [('employee_id', operator, name)] + args, context=context, limit=limit)
        else:
            ids = self.search(cr, uid, [('name', operator, name)] + args, context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)


    _columns = {
        'givenname': fields.char('Given Name', size=40),
        'surname': fields.char('Surname', size=40),
        'givenname_latin': fields.char('Given Name Lat', size=40),
        'surname_latin': fields.char('Surname Lat', size=40),
        'employee_id': fields.integer('Employee ID', required=True),
        'public_employment_date': fields.date('Employment Date'),
        'work_start_date': fields.date('Work Start Date'),
    }
employee()
