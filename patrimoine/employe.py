# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import many2many
class famille(osv.Model):
    _inherit='hr.employee'
    _columns={
              'piece_id':fields.many2one("patrimoine.piece","Bureau"),
              'article_ids':fields.one2many('patrimoine.article','employee_id','Les articles'),
              }