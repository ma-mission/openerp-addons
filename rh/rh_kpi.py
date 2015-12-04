from openerp import addons
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import datetime


class rh_kpi(osv.osv):
	def kpi_IG36_employe(self, cr, uid, ids, context={}):
			ret={}
			res=[]
			obj=self.pool.get("rh.employe")
			ens_ids=obj.search(cr,uid,"[]",context=context)
			for record in self.browse(cr,uid,ids,context=context):
				for rec in obj.browse(cr,uid,ens_ids,context=context):
					if rec.category_id.code == 10:
						dn=datetime.strptime(rec.birthday,"%Y-%m-%d")
						dr=datetime.strptime(rec.date_retraite,"%Y-%m-%d")
						d=dn+timedelta(1826)
						if d>dr:
							res.append(rec.id)
				ret[record.id]=res
			return ret
			
	def kpi_IG36_value(self, cr, uid, ids, context={}):
			res={}
			for rec in self.browse(cr,uid,ids,context=context):
				res[rec.id]=len(rec.employe_ids) or 0
			return  res
	
	_name = 'rh.kpi'
	_columns = {
	'IG36': fields.function(kpi_IG36_value, type="integer", string="IG36",store=True, readonly=True),
	'employe_ids':fields.function(kpi_IG36_employe, "rh.employe", type="one2many",  string="Employes",store=True, readonly=True),
			}
	
rh_kpi();



