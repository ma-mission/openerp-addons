#from openerp import api, fields, models
from openerp.osv import osv,fields
class chercheurs(osv.osv):
    _name='chercheurs'
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('name'),
    'email':fields.char('email'),
    'phone':fields.char('Telephone'),
    'function':fields.char('profile'),
    'responsible':fields.many2one('hr.employee',string='responsible'),
    'active':fields.boolean('active'),
    'structures_ids':fields.many2many('structures','structures_rel',string='Structures'),
    'publication_ids':fields.many2many('publication', 'chercheurs_publication_rel', 'publications',string="publications"),
    'brevets_ids':fields.many2many('brevets', 'chercheurs_brevets_rel','brevets',string="brevets"),
    }
    _defaults={
    'active':True,
    }

class structures(osv.osv):
    _name='structures'
    def _get_chercheurs_ids(self, cr, uid, ids,field_name, arg, context=None):
        result = {}
        
        for record in self.browse(cr, uid, ids, context=context):
            result[record.id] = []
            cr.execute('select chercheurs_id from structures_rel where structures_id=%s'%(record.id,))
            res=cr.fetchall()
            if len(res)>0:
                result[record.id] = [x[0] for x in res]
        return result
    def _get_inv_budget(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            budjet_inv_act=record.budget_inv
            res[record.id] = 0.00
            if record.equipment_ids:
                res[record.id]=budjet_inv_act-record.equipment_ids[0].amount
        return res
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('Intitule'),
    'establishment_id':fields.many2one('res.company',string='Etablissement'),
    'chercheurs_ids':fields.many2many('chercheurs','structures_rel',string='Members'),
    #'chercheurs_id1':fields.function(_get_chercheurs_ids, type='many2many', relation="chercheurs", string="Members"),
    'type_id':fields.many2one('type',string="type"),
    'active':fields.boolean('active'),
    'equipment_ids':fields.one2many('equipment','structure_ids','Equipments et ressousses'),
    'budget_fonc':fields.float('Budget de Fonctionnement'),
    'budget_inv':fields.float("Budget d'investissement"),
    'budget_inv_calc':fields.function(_get_inv_budget, type='float', string="Budget d'investissement",),
    'other_budget':fields.float('Autres Budgets'),
    }
    _defaults={
    'active':True,
    }
   
class establishment(osv.osv):
    _name='establishment'
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('name'),
    'address':fields.text('address'),
    'active':fields.boolean('active'),
    }
    _defaults={
    'active':True,
    }
class type(osv.osv):
    _name='type'
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('type'),
    'active':fields.boolean('active'),
    }
    _defaults={
    'active':True,
    }
class publication(osv.osv):
    _name="publication"
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('title'),
    'type':fields.many2one('publicationtype',string="type"),
    'date':fields.date('date'),
    'publisher':fields.char('publisher'),
    'active':fields.boolean('active'),
    'chercheurs_id':fields.many2one('chercheurs',string="chercheur")
    
    }
    _defaults={
    'active':True,
    }
class publicationtype(osv.osv):
    _name="publicationtype"
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('name'),
    'active':fields.boolean('active'),
    }
    _defaults={
    'active':True,
    }


class brevets(osv.osv):
    _name="brevets"
    _columns={
    'code':fields.integer('id'),
    'title':fields.char('Titre'),
    'registre_date':fields.date("Date denregistrement a l'OMPIC"),
    'reference':fields.integer('Numero de reference'),
    'expiration_date':fields.date("Date d'expiration"),
    'these':fields.boolean('Encedrement de These'),
    'these_title':fields.char('Titre de these'),
    'doctorant':fields.char('doctorant'),
    'encadrant':fields.char('encadrant'),
    'co_encadron':fields.char('Co Encadrant'),
    'ced':fields.char('CED'),
    'signup_date':fields.date("date d'inscription"),
    'link':fields.char('Lien pour Telechargement du rapport'),
    'active':fields.boolean('active'),
    'chercheurs_id':fields.many2one('chercheurs',string="chercheur")
    }
    _defaults={
    'active':True,
    }

class paretenariattype(osv.osv):
    _name="paretenariattype"
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('name'),
    'active':fields.boolean('active'),
    }
    _defaults={
    'active':True,
    }
class paretenariat(osv.osv):
    _name="paretenariat"
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('name'),
    'active':fields.boolean('active'),
    'type':fields.many2one('paretenariattype'),
    'objectif':fields.char('objectif'),
    'duration':fields.char('duration'),
    'responsible':fields.char('responsible'),
    'date_signature':fields.date('date signature'),
    'structures_id':fields.many2one('structures','structures'),
    }
    _defaults={
    'active':True,
    }
    

class equipment(osv.osv):
    _name="equipment"
    _columns={
    'id_equipment':fields.integer('id'),
    'name':fields.char('intitule'),
    'active':fields.boolean('active'),
    'category':fields.many2one('equipment_category','Categorie'),
    'inventory':fields.char("Numero d'inventaire"),
    'structure_ids':fields.many2one('structures','Structures'),
    'quantity':fields.integer('Quantite'),
    'amount':fields.float('Montant'),
    'date_of_sale':fields.date('Commande le'),
    'type_of_budjet':fields.selection([('Invistissement','Invistissement'),('fonctionnement','fonctionnement'),('other','other')],'Type de Budjet'),
    'type_of_sale':fields.selection([('bon de commande','bon de commande'),('marche','marche')],'Type de Commande'),
    }
    _defaults={
    'active':True,
    }

class equipment_category(osv.osv):
    _name="equipment_category"
    _columns={
    'code':fields.integer('id'),
    'name':fields.char('name'),
    'active':fields.boolean('active'),
    }
    _defaults={
    'active':True,
    }
