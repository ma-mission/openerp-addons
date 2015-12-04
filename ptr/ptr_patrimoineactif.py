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

class ptr_patrimoineactif(osv.osv):

	def create(self, cr, uid, vals, context=None):
		cr.execute("SELECT ptractif_ids FROM rh_empolye WHERE id="+str(vals['responsable']))
		ptrgeo=cr.fetchone()[0]
		
		cr.execute("INSERT INTO ptr_patrimoineactif(code,designation,valacqui,dateacqui,dateserv,nbc,nbl,nfact,sousfamille,marque,fournisseur,ptrgeo,responsable)VALUES("\
				   "'"+str(vals['code'])+"','"+str(vals['designation'])+"','"+str(vals['valacqui'])+"','"+str(vals['dateacqui'])+"','"+str(vals['dateserv'])+"'"\
				   ",'"+ str(vals['nbc'])+"','"+str(vals['nbl'])+"','"+str(vals['nfact'])+"','"+str(vals['sousfamille'])+"','"+str(vals['marque'])+"','"+str(vals['fournisseur'])+"'"\
				   ",'"+str(ptrgeo)+"','"+str(vals['responsable'])+"')")
		
	def unlink(self, cr, uid, ids, context=None):
		obj=self.browse(cr,uid,ids,context=None)
		for rec in obj:
			id_sf=rec.sousfamille.id
		cr.execute("SELECT stockmin FROM ptr_sousfamille WHERE id="+str(id_sf))
		stock=cr.fetchone()[0]
		cr.execute("SELECT libelle FROM ptr_sousfamille WHERE id="+str(id_sf))
		lib=cr.fetchone()[0]
		cr.execute("SELECT COUNT(*)-1 FROM ptr_patrimoineactif WHERE sousfamille="+str(id_sf))
		nb=cr.fetchone()[0]
		req="SELECT CURRENT_DATE"
		cr.execute(req)
		d=cr.fetchone()[0]
		if nb<stock:
			cr.execute("INSERT INTO ptr_alertstock(categorie,libelle,masquer,datealerte)VALUES('"+str(lib)+"','Stock insuffisant','NON','"+str(d)+"')")
		return super(ptr_patrimoineactif, self).unlink(cr, uid, ids, context=context)
		
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	_name = 'ptr.patrimoineactif'
	_description = "Classe de patrimoine actif"
	_rec_name = 'designation'
	_columns = {
        'code': fields.char('Code'),
		'designation': fields.char('Designation', required=True),
		'valacqui': fields.char('Val Acqui.'),
		'dateacqui': fields.date('Date Acqui.', required=True),
		'dateserv': fields.date('Date mise serv.', required=True),
		'etatactu': fields.char('Etat Actuel'),
		'nbc': fields.char('N BC'),
		'nbl':fields.char('N BL'),
		'nfact':fields.char('N Fact.'),
		'qttstock':fields.float('Qauantie en stock.'),
		'sousfamille':fields.many2one('ptr.sousfamille','SFamille', required=True),
		'marque':fields.many2one('ptr.marque','Marque', required=True),
		'fournisseur':fields.many2one('ptr.fournisseur','Fournisseur', required=True),
		'ptrgeo':fields.many2one('ptr.patrimoinegeo','Patrimoine geo'),
		'responsable':fields.many2one('rh.employe','Responsable', required=True),
		'image':fields.binary('Image'),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_patrimoineactif': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the actif patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),

					}
ptr_patrimoineactif()

