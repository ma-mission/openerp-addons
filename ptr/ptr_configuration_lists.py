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


class ptr_categoriepersonnel(osv.osv):

	_name = 'ptr.categoriepersonnel'
	_description = "Classe des categories de personnel"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle'),
					}
ptr_categoriepersonnel()



#****************************************

class ptr_famille(osv.osv):

	_name = 'ptr.famille'
	_description = "Classe de Famille"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle'),
					}
ptr_famille()

#*****************************************

class ptr_sousfamille(osv.osv):
	_name = 'ptr.sousfamille'
	_description = "Classe de Sous Famille"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle'),
		'famille':fields.many2one('ptr.famille','Famille'),
		'stkmin':fields.float('Stock Min'),
					}

ptr_sousfamille()

#******************************************
class ptr_marque(osv.osv):
	
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	_name = 'ptr.marque'
	_description = "Classe des marques"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle'),
		'image':fields.binary('Image'),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_unite': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the actif patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
		
					}
ptr_marque()

#*********************************************

class ptr_typeptrgeo(osv.osv):

	_name = 'ptr.typeptrgeo'
	_description = "Classe des type de patrimoines geographique"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle'),
					}
ptr_typeptrgeo()


#*****************************************

class ptr_technicieninterne(osv.osv):

	def ptr_technicieninterne_CheckVolH(self, cr, uid, ids,context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			tmp=rec.volh
			if float(tmp)<0 :
				return False
			return True
	
	
	_name = 'ptr.technicieninterne'
	_description = "Classe des techniciens internes"
	_columns = {
        'nom': fields.char('Nom', required=True),
		'volh': fields.float('Volume Horaire', required=True),
		'intervention':fields.many2one('ptr.intervention','Intervention', ondelete='cascade'),
		}
	_constraints = [
        (ptr_technicieninterne_CheckVolH, 'Error!\nCertains volumes horaires de technicien interne sont negatifs',['volh'])
    ]

ptr_technicieninterne()

#******************************************

class ptr_priorite(osv.osv):
	_rec_name = 'libelle'
	_name = 'ptr.priorite'
	_description = "Classe des prioites des interventions"
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Priorite'),
		}
ptr_priorite()



#******************************************

class ptr_modepaiement(osv.osv):
	_rec_name = 'libelle'
	_name = 'ptr.modepaiement'
	_description = "Classe des modes de paiement"
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Mode Paiement'),
		}
ptr_modepaiement()

#******************************************

class ptr_banque(osv.osv):
	_rec_name = 'libelle'
	_name = 'ptr.banque'
	_description = "Classe des banques"
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Banque'),
		}
ptr_banque()
class ptr_alertstock(osv.osv):

	_name = 'ptr.alertstock'
	_description = "Classe des aletres du stock"
	_columns = {
		'datealerte':fields.char('Date Alerte'),
		'categorie':fields.char('Categorie'),
		'libelle': fields.char('Libelle'),
		'qtestock': fields.float('Qte en Stock'),
		'stockmin': fields.float('Qte en Stock Minimale'),
		'masquer':fields.selection([('OUI','oui'), ('NON','non')],string="Masquer"),
					}
ptr_alertstock()
#****************************************

class ptr_unite(osv.osv):
		
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	_name = 'ptr.unite'
	_description = "Classe des unites"
	_rec_name = 'libelle'
	_columns = {
        'code': fields.char('Code'),
		'libelle': fields.char('Libelle', required=True),
		'idetablissement':fields.many2one('ptr.etablissement','Etablissement'),
		'ptrgeo_ids': fields.one2many('ptr.patrimoinegeo','unite',string='Patrimoin Geo'),
		'image':fields.binary('Image'),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_unite': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the actif patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),

					}

ptr_unite()
#*********************************************


