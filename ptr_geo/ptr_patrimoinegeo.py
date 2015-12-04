from openerp.osv import osv, fields
from openerp import tools

class ptr_patrimoinegeo(osv.osv):
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	_name = 'ptr.patrimoinegeo'
	_description = "Classe de patrimoine geographique"
	_rec_name = 'designation'
	_columns = {
        'code': fields.char('Code'),
		'designation': fields.char('Designation', required=True),
		'croquis': fields.binary('Croquis'),
		'superficie': fields.float('Superficie'),
		'capacite_accueil': fields.float('Capacite Accueil'),
		'ficheimmeuble': fields.binary('Fiche Immeuble'),
		'ficheetage': fields.binary('Fiche Etage'),
		'fichelocal': fields.binary('Fiche Local'),
		'type':fields.many2one('ptr.typeptrgeo','Type Patrimoin'),
		'unite':fields.many2one('ptr.unite','Departement', ondelete='cascade', required=True),
		#'responsable':fields.many2one('rh.employe','Responsable'),
		#'personnel_ids': fields.one2many('rh.employe','office_localisation_id',string='Personnel'),
		'image':fields.binary('Image'),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_patrimoinegeo': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the geographic patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
				 }
ptr_patrimoinegeo()

