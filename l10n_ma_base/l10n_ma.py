# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True, translate=True),
        #'city_id': fields.many2one('res.city', 'City'),
        'chair': fields.char('Chair', size=128, translate=True),
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
