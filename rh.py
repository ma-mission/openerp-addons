from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools



class rh_employee(osv.osv):
	def _get_image(self, cr, uid, ids, name, args, context):
			result = dict.fromkeys(ids, False)
			for obj in self.browse(cr, uid, ids, context=context):
				result[obj.id] = tools.image_get_resized_images(obj.image)
			return result

	def _set_image(self, cr, uid, id, name, value, args, context):
			return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
	
	def _employee_name_get_fnc(self, cr, uid, ids, args=None,fields=None,context=None):
			res = {}
			for record in self.browse(cr, uid, ids, context=context):
				res[record.id] = record['name'] +' '+record['lastname']
			return res
	
	def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
			if not args:
				args = []
			if name.isdigit() and operator in ['=', 'ilike']:
				operator = '='
				ids = self.search(cr, uid, [('employee_id', operator, name)] + args, context=context, limit=limit)
			else:
				ids = self.search(cr, uid, [('name', operator, name)] + args, context=context, limit=limit)
			return self._employee_name_get_fnc(cr, uid, ids, context=context)
			
	def _current_state_get_fnc(self, cr, uid, ids, args,fields,context=None):
			res={}
			obj = self.pool.get('rh.job')
			obj_ids=obj.search(cr, uid, [('employee_id','in',ids)])
			for record in obj.browse(cr, uid, obj_ids, context):
				if record.current_state:
					if fields=='poste_id':
						res[record.employee_id.id]=record[fields].name
					else:
						res[record.employee_id.id]=record[fields]
			return res
	
	_name = 'rh.employee'
	_columns = {
	#tools
		'complete_name': fields.function(_employee_name_get_fnc, type="char", size=255, string='Full name',store=True, readonly=True),
		'count': fields.float("Counter"),
	#personnel informations
		'name_ar': fields.char("Arabic name",size=128),
		'lastname_ar': fields.char("Arabic last name",size=128),
		'name': fields.char("Name",size=128),
		'lastname': fields.char("Last name",size=128),
		'cin': fields.char("CIN",size=128,required=True),
		'passport': fields.char("Passport",size=128),
		'birthday': fields.date("Birthday"),
		'birth_place': fields.char("Place of birth",size=128),
		'gender': fields.selection([('male', 'Male'),('female', 'Female')], 'Gender'),
        'marital': fields.selection([('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status'),
        'num_children': fields.integer("Number of children"),
		'phone': fields.char("Phone number",size=128),
		'adress': fields.text("Adress"),
		'city': fields.char("city", size=128),
		'email': fields.char("Email",size=128),
		'notes': fields.text('Notes'),
	
	#image
		'image': fields.binary("Photo"),
			
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
				string="Medium-sized image", type="binary", multi="_get_image",
				store = {'rh.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),},
					),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
				string="Smal-sized image", type="binary", multi="_get_image",
				store = {'rh.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10), },            
					),	
	
	    
	#work informations
		'establishment_id1': fields.many2one('rh.establishment','Establishment'),
		'department_id': fields.many2one('rh.department',  string='Department'),
		'office_localisation': fields.char("Office localisation"),
		'office_station':fields.integer("Number of station"),
		'work_fleet': fields.char("Work phone",size=128),
		'work_email': fields.char("Work e-mail",size=128),
	#job information
		'doti': fields.integer("S.O.M"),
		'pb': fields.integer("Budget item"),
		'recruitment_date':fields.date("Date of recruitment"),
		
	#Current state
		'poste': fields.function(_current_state_get_fnc,'poste_id', type="char", string='Poste',store=True),
		'category': fields.function(_current_state_get_fnc,'category', type="char", string='Category',store=True),
		'scale': fields.function(_current_state_get_fnc,'scale', type="integer", string='Scale',store=True),
		'echelon': fields.function(_current_state_get_fnc,'echelon', type="integer", string='Echelon',store=True),
		'index': fields.function(_current_state_get_fnc,'index', type="integer", string='Index',store=True),
		'scale_effect_date': fields.function(_current_state_get_fnc,'scale_effect_date', type="date", string='Date of scale effect',store=True),
		'echelon_effect_date': fields.function(_current_state_get_fnc,'echelon_effect_date', type="date", string='Date of echelon effect',store=True),
		'job_state': fields.function(_current_state_get_fnc,'job_state', type="selection", string='Job State',store=True),
		
	#Proposal state
		'poste_prop': fields.char("Proposal Poste "),
		'category_prop': fields.char("Proposal category"),
		'scale_prop': fields.integer("Proposal scale"),
		'echelon_prop': fields.integer("Proposal echelon"),
		'next_prop_date': fields.date("Date of next proposal"),
		
	#History
		'poste_ids': fields.one2many('rh.job', 'employee_id', 'Postes'),
		
	#Studies
		'studies_ids': fields.one2many('rh.diploma', 'employee_id', 'Diploma'),
	#docs
		'docs_ids': fields.one2many('rh.employee.request', 'applicant_id', 'Documents'),
			}
	_defaults = {
			 'count': 1.00,
					}
	_sql_constraints = [('cin_uniq', 'unique (cin)','The CIN of the employee must be unique !')]
	_sql_constraints = [('doti_uniq', 'unique (doti)','The S.O.M of the employee must be unique !')]
	_sql_constraints = [('pb_uniq', 'unique (pb)','The Budget Item of the employee must be unique !')]
	
	
	def create(self, cursor, user, vals, context=None):
		if 'cin' in vals:
			vals['cin'] = vals['cin'].upper()
		if 'name' in vals:
			vals['name'] = vals['name'].upper()
		if 'lastname' in vals:
			vals['lastname'] = vals['lastname'].title()
		return super(rh_employee, self).create(cursor, user, vals,context=context)
	
	def write(self, cursor, user, ids, vals, context=None):
		if 'cin' in vals:
			vals['cin'] = vals['cin'].upper()
		if 'name' in vals:
			vals['name'] = vals['name'].upper()
		if 'lastname' in vals:
			vals['lastname'] = vals['lastname'].title()
		return super(rh_employee, self).write(cursor, user, ids, vals,context=context)
	
	_order = "complete_name"
	_rec_name = "complete_name"
rh_employee();



