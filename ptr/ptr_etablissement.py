import csv
import psycopg2
import openerp.exceptions
from openerp.osv import osv, fields,orm
from openerp import tools
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _


class ptr_etablissement(osv.osv):


	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
	
			
	_name = 'ptr.etablissement'
	_description = "Classe des etablissements"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle', required=True),
		'unite_ids': fields.one2many('ptr.unite','idetablissement',string='Departement'),
		'inventaire_ids': fields.one2many('ptr.inventaire','etablissement',string='Inventaire'),
		'intervention_ids': fields.one2many('ptr.intervention','etablissement',string='Intervention'),
		'image':fields.binary('Image'),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_etablissement': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the actif patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),

					}

ptr_etablissement()