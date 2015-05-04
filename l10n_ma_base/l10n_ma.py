# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True, translate=True),
        #'city_id': fields.many2one('res.city', 'City'),
    }

res_partner()

class res_city(osv.osv):
    _name = 'res.city'

    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True, translate=True),
        'state_id': fields.many2one('res.country.state', 'State'),
        'country_id': fields.related('state_id', 'country_id', type='many2one',# readOnly=True,
                                     relation='res.country', string='Country'),
    }

res_city()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
