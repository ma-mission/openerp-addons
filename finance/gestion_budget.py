# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import datetime
from openerp import netsvc

class exercice(osv.osv):
    _name = "b.exercice"
    _description = ""
    _rec_name = "year"
       

    _columns = {
        'year': fields.integer('Année'),
            }

    _defaults = {
       
    }

exercice()

class axe(osv.osv):
    _name = "b.axe"
    _description = ""
    _rec_name = "desig"
       

    _columns = {
        'desig': fields.char('Axe designation', size=200, required=True),
        'saxe_ids' : fields.one2many('b.saxe','axe_id','Sous-axe'),
            }

    _defaults = {
       
    }

axe()

class sous_axe(osv.osv):
    _name = "b.saxe"
    _description = ""
    _rec_name = "desig"
       
    _columns = {
        'axe_id' : fields.many2one('b.axe', 'Axe'),
        'desig': fields.char('Sous-axe designation', size=200, required=True),
            }

    _defaults = {
       
    }

sous_axe()

class compte(osv.osv):
    _name = "b.compte"
    _description = ""
    _rec_name = "code"
       

    _columns = {
        'code': fields.integer('Code du compte'),
        'desig': fields.char('Designation', size=200, required=True),
            }

    _defaults = {
       
    }

compte()


class vbudget(osv.osv):
     _name = "b.vbudget"
     _description = ""
     _rec_name = "version"
       

     _columns = {
        'version': fields.integer('Version du budget', readonly=True),
        'type':fields.selection([('fon', 'Fonctionnement'),('inv', 'Investissement')], 'Type'),
        'exercice': fields.many2one('b.exercice' ,'Exercice'),
        'etab': fields.char('Etablissement', size=200),
        'saxe_ids' : fields.one2many('b.credit','saxe','Sous-Axes'),
        'state': fields.selection([('draft', 'Budget brouillon'), ('accepted', 'Validé'), ('expired', 'Expiré'), ('refuse', 'Annulé')], 'Status', readonly=True, track_visibility='onchange'),
                }

     _defaults = {
            'version': 1,     
            'state': 'draft',
        }
    
     def ao_accepted(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'accepted'})
    
     def ao_refuse(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'refuse'})
    
     def ao_expired(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'expired'})
    
vbudget()

class credit(osv.osv):
     _name = "b.credit"
     _description = ""
     _rec_name = "montant"
       

     _columns = {
                 
        'saxe_id': fields.many2one('b.saxe' ,'Sous-Axe'),
        'saxe':fields.many2one('b.vbudget', 'Sous-Axe'),
        'montant': fields.float('Montant total', digits=(9,3)),
            }

     _defaults = {
       
    }
    
credit()

class details_credit(osv.osv):
     _name = "b.det.credit"
     _description = ""
     _rec_name = "montant"
       

     _columns = {
                 
        'saxe_id': fields.many2one('b.saxe' ,'Sous-Axe'),
        'compte': fields.many2one('b.compte','Compte'),
        'montant': fields.float('Montant total', digits=(9,3)),
            }

     _defaults = {
       
    }
    
credit()
    
class article(osv.osv):
    _name = "b.article"
    _description = ""
    _rec_name = "nom"
       

    _columns = {
        'code': fields.integer('Article code'),
        'nom': fields.char('Nom', size=200, required=True),
        'desc': fields.text('Description', required=True),
        'categ':fields.char('Catégorie', size=200, required=True),
        'prixest':fields.float('Prix estimatif', digits=(9,2)),
        
            }

    _defaults = {
    }

article()

class nature(osv.osv):
    _name = "b.nature"
    _description = ""
    _rec_name = "desig"
       

    _columns = {
        'code': fields.integer('Nature code'),
        'desig': fields.char('Designation', size=200, required=True),
        'montant': fields.float('Montant max', digits=(9,2)),
        'total' : fields.float('Montant total', digits=(9,2)),

            }

    _defaults = {
       'montant': 250000 ,
    }

nature()

class appel_of(osv.osv):
    _name = "b.appelof"
    _description = ""
    _rec_name = "code"
    
    
    def m_brut(self, cr, uid, ids, name, args, context=None):
            res = {}
            for appel_of in self.browse(cr, uid, ids):
                total =0
                for ligne in appel_of.ligne_ids:
                    total = total + (ligne.prixest * ligne.quantite)
                res[appel_of.id]= total
            return res 
         
    def taxe(self, cr, uid, ids, name, args, context=None): 
         res = {}
         for appel_of in self.browse(cr, uid, ids):
                res[appel_of.id] = ( appel_of.brut * 20 ) / 100 
         return res
     
    def total(self, cr, uid, ids, name, args, context=None): 
         res = {}
         for appel_of in self.browse(cr, uid, ids):
                res[appel_of.id] = appel_of.brut - appel_of.taxe 
         return res
   

    _columns = {
        'code':fields.integer('Code d\'engagement'),
        'nature': fields.many2one('b.nature' ,'Nature'),
        'compte': fields.many2one('b.compte' ,'Compte'),
        'axe': fields.many2one('b.axe' ,'axe'),
        'exercice': fields.many2one('b.exercice' ,'Exercice'),
        'sousaxe': fields.many2one('b.saxe' ,'Sous-axe'),
        'ligne_ids': fields.one2many('b.ligne.appelof' ,'ligne_id','Articles'),
        'lignef_ids': fields.one2many('b.lignef.appelof' ,'lignef_id','Fournisseur'),
        'ligned_ids': fields.one2many('b.ligned.appelof' ,'ligned_id','Devis'),
        'pv': fields.binary('P.V'),
        'brut':fields.function(m_brut, type='float', string='Montant brut'),
        'taxe':fields.function(taxe, type='float', string='Taxe'),
        'total':fields.function(total, type='float', string='Montant net'),
        'state': fields.selection([('draft', 'Consultation'), ('sent', 'Demande envoyée'), ('received', 'Offre reçue'), ('validate', 'Confirmé'), ('refuse', 'Engagement annulé')], 'Status', readonly=True, track_visibility='onchange'),
            }

    _defaults = {
            'state': 'draft',
    }
    
    def ao_validate(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'validate'})
    
    def ao_sent(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'sent'})
    
    def ao_received(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'received'})

    def ao_refuse(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'refuse'})

    def ao_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'})
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the request for quotation and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'b.appelof', ids[0], 'send_rfq', cr)
        datas = {
                 'model': 'b.appelof',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'purchase.quotation', 'datas': datas, 'nodestroy': True}
appel_of()

class ligne_appel_of(osv.osv):
    _name = "b.ligne.appelof"
    _description = ""
    _rec_name = "article"
       
         
    def totaal(self, cr, uid, ids, name, args, context=None): 
         res = {}
         for ligne_appel_of in self.browse(cr, uid, ids):
                res[ligne_appel_of.id] = ligne_appel_of.prixest * ligne_appel_of.quantite
         return res

    _columns = {
        'ligne_id': fields.many2one('b.appelof','Nature'),
        'article': fields.many2one('b.article', 'Article'),
        'desc': fields.char('Description', size=200, required=True),
        'prixest': fields.float('Prix unitaire', digits=(9,2)),
        'quantite':fields.integer('Quantité'),
        'prixtotal':fields.function(totaal, type='float', string='Prix total'),
        
            }

    _defaults = {
      
    }

ligne_appel_of()

class ligned_appel_of(osv.osv):
    _name = "b.ligned.appelof"
    _description = ""
    _rec_name = "code"
       

    _columns = {
        'ligned_id': fields.many2one('b.appelof','Devis'),
        'code': fields.integer('Code'),
        'devis': fields.binary('Devis'),
        
            }

    _defaults = {
      
    }

ligned_appel_of()


class lignef_appel_of(osv.osv):
    _name = "b.lignef.appelof"
    _description = ""
    _rec_name = "fournisseur"
       

    _columns = {
        'lignef_id': fields.many2one('b.appelof','Nature'),
        'fournisseur': fields.many2one('res.partner', 'Fournisseurs'),
        
            }

    _defaults = {
      
    }

lignef_appel_of()


class engagement(osv.osv):
    _name = "b.engagement"
    _description = ""
    _rec_name = "num"
       

    _columns = {
        'num': fields.integer('Numéro d\'engagement'),
        'exercice': fields.many2one('b.exercice' ,'Exercice'),
        'typ':fields.selection([('fon', 'Fonctionnement'),('inv', 'Investissement')], 'Type de budget'),
        'compte': fields.many2one('b.compte' ,'Compte'),
        'axe': fields.many2one('b.axe' ,'Axe'),
        'sousaxe': fields.many2one('b.saxe' ,'Sous-axe'),
        'type': fields.selection([('om', 'Ordre de mission'),('ma', 'Marché'),('hs', 'Heures supplémentaires')], 'Type d\'engagement'),
        'nature': fields.many2one('b.nature' ,'Nature'),
        'benef':fields.many2one('res.partner' ,'Bénéficiaire'),
        'mnt': fields.float('Montant engagé', digits=(9,2)),

            }

    _defaults = {
       
    }

engagement()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
