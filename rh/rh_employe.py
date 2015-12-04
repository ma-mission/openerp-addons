from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from datetime import datetime
from datetime import timedelta



class rh_employe(osv.osv):
	def name_get(self, cr, uid, ids, context={}):
			if not len(ids):
				return []
			res=[]
			for record in self.browse(cr, uid, ids,context=context):
				res.append((record.id, record.name + ' ' + record.lastname))     
			return res
	def _employe_retraite_get_fnc(self, cr, uid, ids, args=None,fields=None,context=None):
			res={}
			for record in self.browse(cr, uid, ids,context=context):
				dn=datetime.strptime(record.birthday,"%Y-%m-%d")
				dr=dn+timedelta(23740)
				res[record.id]=datetime.strftime(dr,"%Y-%m-%d")
			return res
			
	def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
			if not args:
				args = []
			if name.isdigit() and operator in ['=', 'ilike']:
				operator = '='
				ids = self.search(cr, uid, [('employe_id', operator, name)] + args, context=context, limit=limit)
			else:
				ids = self.search(cr, uid, [('name', operator, name)] + args, context=context, limit=limit)
			return self.name_get(cr, uid, ids, context=context)
			
	def _get_image(self, cr, uid, ids, name, args, context):
			result = dict.fromkeys(ids, False)
			for obj in self.browse(cr, uid, ids, context=context):
				result[obj.id] = tools.image_get_resized_images(obj.image)
			return result

	def _set_image(self, cr, uid, id, name, value, args, context):
			return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
	
	def _employe_name_get_fnc(self, cr, uid, ids, args=None,fields=None,context=None):
			res = {}
			tmp_str=''
			for record in self.browse(cr, uid, ids, context=context):
				if record.name:
					tmp_str= record.name
				if record.lastname:
					tmp_str= tmp_str+' '+record.lastname
				res[record.id]=tmp_str
				tmp_str=''
			return res
	
	
	def _get_emolument_lines(self, cr, uid, ids, name, arg, context=None):
			line_obj = self.pool.get('rh.salary')
			res = {}
			for employe in self.browse(cr, uid, ids, context=context):
				line_ids = line_obj.search(cr, uid,[
					('rubrique_id.code', '<', 4000),
					('employe_id', '=', employe.id),
					('annee','=',employe.annee_id.annee),
					('mois','=',employe.mois)
					])
				res[employe.id] = line_ids
			return res		
	def _get_retenue_lines(self, cr, uid, ids, name, arg, context=None):
			line_obj = self.pool.get('rh.salary')
			res = {}
			for employe in self.browse(cr, uid, ids, context=context):
				line_ids = line_obj.search(cr, uid,[
					('rubrique_id.code', '>', 4000),
					('employe_id', '=', employe.id),
					('annee','=',employe.annee_id.annee),
					('mois','=',employe.mois)
					])
				res[employe.id] = line_ids
			return res		
	def _get_brut_annuel(self, cr, uid, ids, name, arg, context=None):
			line_obj = self.pool.get('rh.salary')
			res = {}
			total=0.0
			for employe in self.browse(cr, uid, ids, context=context):
				line_ids=self._get_emolument_lines(cr,uid,ids,None,None)
				for line in line_obj.browse(cr,uid,line_ids[employe.id],context=context):
					total=total+line.price
				res[employe.id] = total
				
			return res		
	
	def _get_retenues(self, cr, uid, ids, name, arg, context=None):
			line_obj = self.pool.get('rh.salary')
			res = {}
			total=0.0
			for employe in self.browse(cr, uid, ids, context=context):
				line_ids=self._get_retenue_lines(cr,uid,ids,None,None)
				for line in line_obj.browse(cr,uid,line_ids[employe.id],context=context):
					total=total+line.price
				res[employe.id] = total
			return res		
	def _get_net_annuel(self, cr, uid, ids, name, arg, context=None):
			res = {}
			total=0.0
			for employe in self.browse(cr, uid, ids, context=context):
				total=employe.brut_annuel - employe.retenues
				res[employe.id] = total
			return res		
	def _get_net_mensuel(self, cr, uid, ids, name, arg, context=None):
			res = {}
			total=0.0
			for employe in self.browse(cr, uid, ids, context=context):
				res[employe.id] = employe.brut_annuel/12
			return res	
	
	def _get_categorie_name(self, cr, uid, ids, name, arg, context=None):
			for employe in self.browse(cr, uid, ids, context=context):
				for fonction in employe.fonction_ids:
					if fonction.state == 'A':
						return {employe.id:fonction.id}
			return False	
	

	def onchange_etablissement(self,cr,uid,ids, arg,context=None):
			obj = self.pool.get('ptr.unite')
			dep_ids = obj.search(cr,uid, [('idetablissement','=',arg)],context)
			return {'domain':{'departement_id':[('id','in',dep_ids)]}}
	
	def onchange_departement(self,cr,uid,ids, arg,context=None):
			obj = self.pool.get('ptr.patrimoinegeo')
			dep_ids = obj.search(cr,uid, [('unite','=',arg)],context)
			return {'domain':{'office_localisation_id':[('id','in',dep_ids)]}}
	_name = 'rh.employe'
	_columns = {
	#tools
		'name': fields.char("Name",size=128),
		'complete_name': fields.function(_employe_name_get_fnc, type="char", string="Full name",store=True, readonly=True),
	#personnel informations
		'name_ar': fields.char("Arabic name",size=128),
		'lastname_ar': fields.char("Arabic last name",size=128),
		'lastname': fields.char("Last name",size=128),
		'cin': fields.char("CIN",size=128),
		'pays_id': fields.many2one("res.country",'Pays'),
		'passport': fields.char("Passport",size=128),
		'birthday': fields.date("Birthday"),
		'birthday_state': fields.boolean("Estime"),
		'birth_place': fields.char("Place of birth",size=128),
		'gender': fields.selection([('M', 'Male'),('F', 'Female')], 'Gender'),
        'marital': fields.selection([('C', 'Single'), ('M', 'Married'), ('V', 'Widower'), ('D', 'Divorced')], 'Marital Status'),
        'num_children': fields.integer("Number of children"),
		'phone': fields.char("Phone number",size=128),
		'adress': fields.text("Adress"),
		'city_id': fields.many2one("rh.ville", "City"),
		'email': fields.char("Email",size=128),
		'notes': fields.text('Notes'),
	
	#image
		'image': fields.binary("Photo"),
			
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
				string="Medium-sized image", type="binary", multi="_get_image",
				store = {'rh.employe': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),},
					),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
				string="Smal-sized image", type="binary", multi="_get_image",
				store = {'rh.employe': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10), },            
					),	
	
	    
	#work informations
		'etablissement_id': fields.many2one('ptr.etablissement','Etablissement'),
		'departement_id': fields.many2one('ptr.unite',  string='Deparetment'),
		'office_localisation_id': fields.many2one('ptr.patrimoinegeo','Office localisation'),
		'office_station':fields.integer("Number of station"),
		'work_fleet': fields.char("Work phone",size=128),
		'work_email': fields.char("Work e-mail",size=128),
	#job information
		'som': fields.integer("S.O.M"),
		'pb': fields.integer("Budget item"),
		'recrutement_date':fields.date("Date of recrutement"),
		'echelon_date_rel':fields.date("Last modification date"),
		'deduction_rel':fields.integer("Deductions"),
		'fonction_ids': fields.one2many('rh.fonction','employe_id','Fonctions'),
		'category_id': fields.many2one('rh.fonction.category','Category'),
		'corps_id': fields.many2one('rh.fonction.corps','Corps'),
		'cadre_id': fields.many2one('rh.fonction.cadre','Cadre'),
		'grade_id': fields.many2one('rh.fonction.grade','Grade'),
		'organisme_id': fields.integer('Organisme code'),
		'date_retraite': fields.function(_employe_retraite_get_fnc, type="date", string="Date de retraite",store=True, readonly=True),
	#salraire
		'emolument_ids': fields.function(_get_emolument_lines, relation="rh.salary", method=True, type="one2many"),
		'retenue_ids': fields.function(_get_retenue_lines, relation="rh.salary", method=True, type="one2many"),
		'mois':fields.selection([
								 ('01', 'Janvier'),
								 ('02', 'Fevrier'),
								 ('03', 'Mars'),
								 ('04', 'Avril'),
								 ('05', 'Mai'),
								 ('06', 'Juin'),
								 ('07', 'Juillet'),
								 ('08', 'Aout'),
								 ('09', 'Septembre'),
								 ('10', 'Octobre'),
								 ('11', 'Nevembre'),
								 ('12', 'Decembre')
								  ], 'Mois'),
		'annee_id':fields.many2one("rh.annee","Annee"),
		'brut_annuel': fields.function(_get_brut_annuel,type="float", method=True, string="Brut annuel"),
		'retenues': fields.function(_get_retenues,type="float", method=True, string="Total des Retenues"),
		'net_annuel': fields.function(_get_net_annuel,type="float", method=True, string="Net annuel"),
		'net_mensuel': fields.function(_get_net_mensuel,type="float", method=True, string="Net mensuel"),
	#ordre de mission
		'ordre_mission_ids':fields.many2many("rh.ordre_mission","ordre_mission_employe_rel","rh_employe_id","rh_ordre_mission_id",string="Ordres de mission"),
	#etudes et qualification
		'qualification_ids': fields.one2many('rh.study','qualification_id'),
	#Demmande d'attestation
		'demande_ids': fields.one2many('rh.demande','employe_id',string="Demandes"),
	#Patrimoine Actif Associe
		'ptractif_ids': fields.one2many('ptr.patrimoineactif','responsable',string='Patrimoin Actif'),
	}
	_defaults = {
				
					}
	_sql_constraints = [('cin_uniq', 'unique (cin)','The CIN of the employe must be unique !')]
	_sql_constraints = [('som_uniq', 'unique (som)','The S.O.M of the employe must be unique !')]
	_sql_constraints = [('pb_uniq', 'unique (pb)','The Budget Item of the employe must be unique !')]
	
	
	def create(self, cursor, user, vals, context=None):
		if 'cin' in vals:
			vals['cin'] = vals['cin'].upper()
			vals['cin'] = vals['cin'].replace(" ","")
		if 'name' in vals:
			vals['name'] = vals['name'].upper()
		if 'lastname' in vals:
			vals['lastname'] = vals['lastname'].title()
		return super(rh_employe, self).create(cursor, user, vals,context=context)
	
	def write(self, cursor, user, ids, vals, context=None):
		if 'cin' in vals:
			vals['cin'] = vals['cin'].upper()
			vals['cin'] = vals['cin'].replace(" ","")
		if 'name' in vals:
			vals['name'] = vals['name'].upper()
		if 'lastname' in vals:
			vals['lastname'] = vals['lastname'].title()
		return super(rh_employe, self).write(cursor, user, ids, vals,context=context)
	
	_order = "complete_name"
	_rec_name = "complete_name"
	
rh_employe();



