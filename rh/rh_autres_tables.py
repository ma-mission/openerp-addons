from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools


class rh_ville(osv.osv):
	
	_name = 'rh.ville'
	_columns = {
		'province_id': fields.many2one("rh.province","Province"),
		'name': fields.char("Name",size=128),
		'code': fields.integer('Code'),
		'zone': fields.selection([('A ', 'A '), ('B ', 'B '),('C ', 'C ')], 'Zone'),
		'zip': fields.integer('Zip Code'),
		}
rh_ville();
class rh_province(osv.osv):
	
	_name = 'rh.province'
	_columns = {
		'region_id': fields.many2one("rh.region","Region"),
		'name': fields.char("Name",size=128),
		'code': fields.integer('Code'),
		'ville_ids':fields.one2many("rh.ville","province_id","Villes"),
		}
rh_province();

class rh_region(osv.osv):
	
	_name = 'rh.region'
	_columns = {
		'name': fields.char("Name",size=128),
		'code': fields.integer('Code'),
		'province_ids':fields.one2many("rh.province","region_id","Provinces"),
		}
rh_ville();

class rh_moyen_transport(osv.osv):
	
	_name = 'rh.moyen_transport'
	_columns = {
		'name': fields.char("Name",size=128),
		}
rh_moyen_transport();

class rh_rubrique(osv.osv):
	
	_name = 'rh.rubrique'
	_columns = {
		'name': fields.char("Name",size=128),
		'code': fields.integer("Code",size=4),
		}
rh_rubrique();
class rh_annee(osv.osv):
	
	_name = 'rh.annee'
	_columns = {
		'annee': fields.integer("Annee"),
		}
	_rec_name="annee"
rh_annee();

class rh_qualification(osv.osv):
	
	_name = 'rh.qualification'
	_columns = {
		'name': fields.char("Name",size=128),
		}
	
rh_qualification();
class rh_et_type(osv.osv):
	
	_name = 'rh.et_type'
	_columns = {
		'name': fields.char("Name"),
		}
	
rh_et_type();