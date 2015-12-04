from openerp.osv import osv, fields
from openerp import tools

class ptr_personnel(osv.osv):
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	_name = 'ptr.personnel'
	_description = "Classe de personnel"
	_rec_name = 'nom'
	_columns = {
        'matricule': fields.char('Matricule', required=True),
		'nom': fields.char('Nom',required=True),
		'prenom': fields.char('Prenom', required=True),
		'fonction': fields.char('Fonction'),
		'tel': fields.char('Tel'),
		'fax': fields.char('Fax'),
		'email': fields.char('Email'),
		'categorie':fields.many2one('ptr.categoriepersonnel','Categorie', required=True),
		'patrimoinegeo':fields.many2one('ptr.patrimoinegeo','Patrimoine Geo', ondelete='cascade',required=True),
		'ptractif_ids': fields.one2many('ptr.patrimoineactif','responsable',string='Patrimoin Actif'),
		'image':fields.binary('Image'),
		
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_personnel': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the actif patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
				 }
		
ptr_personnel()