from openerp.osv import osv, fields
from openerp import tools

class ptr_fournisseur(osv.osv):
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
		
	_name = 'ptr.fournisseur'
	_description = "Classe de Fournisseur"
	_rec_name = 'denomination'
	_columns = {
        'code': fields.char('Code'),
		'denomination': fields.char('Denomination', required=True),
		'adresse': fields.text('Adresse'),
		'tel': fields.char('Tel'),
		'fax': fields.char('Fax'),
		'email': fields.char('E-mail'),
		'nom_resp': fields.char('Nom Responsable'),
		'prenom_resp': fields.char('Prenom Responsable'),
		'GSM1': fields.char('GSM1'),
		'GSM2': fields.char('GSM2'),
		'image':fields.binary('Image'),
		
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store = {
                'ptr_fournisseur': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the actif patrimoin. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),

		
					}
ptr_fournisseur()

