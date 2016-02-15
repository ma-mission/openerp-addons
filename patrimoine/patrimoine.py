# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import logging
_logger = logging.getLogger('valider_sortie')

class famille(osv.Model):
    _name='patrimoine.famille'
    _columns={
              'name':fields.char('Libellé',size=64,required=True),
              
              }
class sous_famille(osv.Model):
    _name='patrimoine.sous_famille'
    def _qte(self, cr, uid, ids, name, args, context=None): 
         res = {}
         magazin_ids = self.pool.get('patrimoine.piece').search(cr,uid,[('type','=','magazin')])
         for sous_famille in self.browse(cr, uid, ids):
             qte = self.pool.get('patrimoine.article').search(cr,uid,[
                                                                ('sous_famille_id','=',sous_famille.id),
                                                                ('piece_id','in',magazin_ids),
                                                                ],count=True)
             res[sous_famille.id] = qte 
         return res   
    _columns={
              'name':fields.char('Libellé',size=64,required=True),
              'qtm':fields.integer('Quantité minimale'),
              'image':fields.binary('Image',filters='*.png,*.gif,*.jpg'),
              'famille_id':fields.many2one('patrimoine.famille','Famille'),
              'categorie_id':fields.many2one('patrimoine.categorie','Catégorie'),
              'qte':fields.function(_qte, type='integer', string='Quantité'),
              }
    
    
    
class categorie(osv.Model):
    _name='patrimoine.categorie'
    _columns={
              'name':fields.char('Catégorie',size=64,required=True), 
              }
    
    
    
class article(osv.Model):
    _name='patrimoine.article'
    _columns={
              'name':fields.char('Désignation',size=64,required=True),
              'num_inv':fields.char('Numéro inventaire',size=64),
              'num_serie':fields.char('Numéro de série',size=64),
              'sous_famille_id':fields.many2one('patrimoine.sous_famille','Sous Famille'),
              'reception_id':fields.many2one('patrimoine.reception.article','reception'),
              'piece_id':fields.many2one('patrimoine.piece','Pièce'),
              'employee_id':fields.many2one('hr.employee','Employé'),
              }


class reception_article(osv.Model):
    _name='patrimoine.reception.article'

    def _qte(self,cr,uid,ids,name,args,context=None):
        res = {}
        for reception_article in self.browse(cr,uid,ids,context):
            res[reception_article.id] = len(reception_article.article_ids)
        return res

    _columns={        
              'partner_id':fields.many2one('res.partner' ,'Fournisseur'),
              'qte':fields.function(_qte, type='integer', string='Quantité livrée'),
              'sous_famille_id':fields.many2one('patrimoine.sous_famille','Sous famille'),
              'article_ids' : fields.one2many('patrimoine.article','reception_id','Articles'),
              'reception_id':fields.many2one('patrimoine.reception','reception'),
              }

    def on_change_articles(self,cr,uid,ids,article_ids,context=None):
        articles = self.resolve_2many_commands(cr, uid, 'article_ids', article_ids)
        qte = len(article_ids)
        return {'value':{'qte': qte}}
        

class reception(osv.Model):
    _name='patrimoine.reception'
    _columns={        
              'partner_id':fields.many2one('res.partner' ,'Fournisseur',
                      domain=[('is_company','=',True),('supplier','=',True)],
                      context={'default_is_company':True, 'default_supplier':True}),
              'bon_livraison':fields.binary('Bon de livraison',filters='*.png,*.gif,*.jpg,*.pdf'),
              'date_livraison':fields.date('Date de livraison'),
              'reception_article_ids' : fields.one2many('patrimoine.reception.article','reception_id','Articles'),
              }
    
class site(osv.Model):
    _name='patrimoine.site'
    _columns={
              'name':fields.char('Le nom du site',size=64,required=True),
              'adresse':fields.char('L\'adresse du site',size=64),
              'ville_id':fields.many2one('res.city','Ville'),
              'image':fields.binary('photo de satellite',filters='*.png,*.gif,*.jpg'),
              }
class batiment(osv.Model):
    _name='patrimoine.batiment'
    _columns={
              'name':fields.char('Le nom du batiment',size=64,required=True),
              'adresse':fields.char('L\'adresse du batiment',size=64),
              'company_id':fields.many2one('res.company','l\'établissement'),
              'image':fields.binary('Image du batiment',filters='*.png,*.gif,*.jpg'),
              'croqui':fields.binary('Croqui',filters='*.png,*.gif,*.jpg,*.pdf'),
              'nombre':fields.integer('Nombre d\'étages'),
              'piece_ids' : fields.one2many('patrimoine.piece','batiment_id','Pièces'),
              }
class piece(osv.Model):
    _name='patrimoine.piece'
    _columns={
              'name':fields.char('Numéro',size=64,required=True),
              'superficie':fields.integer('Superficie'),
              'batiment_id':fields.many2one('patrimoine.batiment','Bâtiment'),
              'etage':fields.integer('L\'étage'),
              'type':fields.selection([('bureau','Bureau'),('magazin','Magazin'),('salle de réunion','Salle'),('autre','Autre')],'Type'),
              'employee_ids' : fields.one2many('hr.employee','piece_id','Les employées'),
              }
class sortie(osv.Model):
    _name='patrimoine.sortie'
    _columns={        
              'employee_id':fields.many2one('hr.employee' ,'Employé'),
              'article_ids' : fields.many2many('patrimoine.article', 'patrimoine_sortie_article_rel','sortie_id', 'article_id', 'Articles'),
              'decharge':fields.binary('Décharge',filters='*.png,*.gif,*.jpg,*.pdf'),
              'date':fields.date('Date'),
              'state':fields.selection([('draft','Brouillon'),('valid','Validée')], 'Etat'),
              }
    _defaults={
               'state': 'draft',
               }
    def valider(self,cr,uid,ids,context=None):
        for sortie in self.browse(cr,uid,ids,context):
            _logger.info('décharge = %s' % (repr(sortie.decharge),))
            if not sortie.decharge:
                raise osv.except_osv(('Erreur'), (u'Vous devez d\'abord scanner la décharge!' ) )
            for article in sortie.article_ids:
                article.write(
                        {'employee_id': sortie.employee_id.id,
                         'piece_id': sortie.employee_id.piece_id.id,
                         },context=context)
            sortie.write({'state': 'valid'})
class fourniture(osv.Model):
    _name='patrimoine.fourniture'
    def _qte(self,cr,uid,ids,name,args,context=None):
        res = {}
        for fourniture_id in ids: # in self.browse(cr,uid,ids,context):
            reception_ids = self.pool.get('patrimoine.receptionfourniture.ligne').search(cr, uid,
                    [('fourniture_id','=',fourniture_id)])
            receptions = self.pool.get('patrimoine.receptionfourniture.ligne').browse(cr,uid, reception_ids)
            qte_recue = sum(reception.qte for reception in receptions) or 0 # if reception.receptionfourniture_id.state=='valid')
            cr.execute('''SELECT SUM(SL.qte)
             FROM patrimoine_sortiefourniture_ligne SL
             JOIN patrimoine_sortiefourniture S ON(S.id = SL.sortiefourniture_id)
             WHERE SL.fourniture_id = %d AND S.state='valid'
             ''' % (fourniture_id,))
            qte_sortie = cr.fetchone()[0] or 0
            _logger.info(repr(qte_sortie))
            res[fourniture_id] = qte_recue - qte_sortie
        return res
    _columns={
              'name':fields.char('Désignation',size=64,required=True),
              'qtm':fields.integer('Quantité minimale'),
              'image':fields.binary('Image',filters='*.png,*.gif,*.jpg'),
              'qte':fields.function(_qte, type='integer', string='Quantité', readonly=True),
              }

class sortiefourniture(osv.Model):
    _name='patrimoine.sortiefourniture'
    _columns={        
              'employee_id':fields.many2one('hr.employee' ,'Employé'),
              'decharge':fields.binary('Décharge',filters='*.png,*.gif,*.jpg,*.pdf'),
              'date':fields.date('Date'),
              'state':fields.selection([('draft','Brouillon'),('valid','Validée')], 'Etat'),
              'ligne_ids' : fields.one2many('patrimoine.sortiefourniture.ligne','sortiefourniture_id','Fournitures'),
              }
    _defaults={
               'state': 'draft',
               }
    def valider(self,cr,uid,ids,context=None):
        for sortiefourniture in self.browse(cr,uid,ids,context):
            _logger.info('décharge = %s' % (repr(sortiefourniture.decharge),))
            if not sortiefourniture.decharge:
                raise osv.except_osv(('Erreur'), (u'Vous devez d\'abord scanner la décharge!' ) )
            sortiefourniture.write({'state': 'valid'})
            
class sortiefourniture_ligne(osv.Model):
    _name='patrimoine.sortiefourniture.ligne'
    _columns={        
              'qte':fields.integer('Quantité'),
              'fourniture_id':fields.many2one('patrimoine.fourniture','Fourniture'),
              'sortiefourniture_id':fields.many2one('patrimoine.sortiefourniture','sortiefourniture'),
              }            
class receptionfourniture(osv.Model):
    _name='patrimoine.receptionfourniture'
    _columns={        
              'partner_id':fields.many2one('res.partner' ,'Fournisseur',
                      domain=[('is_company','=',True),('supplier','=',True)],
                      context={'default_is_company':True, 'default_supplier':True}),
              'bon_livraison':fields.binary('Bon de livraison',filters='*.png,*.gif,*.jpg,*.pdf'),
              'date_livraison':fields.date('Date de livraison'),
              'ligne_ids' : fields.one2many('patrimoine.receptionfourniture.ligne','receptionfourniture_id','Fournitures'),
              }
class receptionfourniture_ligne(osv.Model):
    _name='patrimoine.receptionfourniture.ligne'
    _columns={        
              'qte':fields.integer('Quantité'),
              'fourniture_id':fields.many2one('patrimoine.fourniture','Fourniture'),
              'receptionfourniture_id':fields.many2one('patrimoine.receptionfourniture','receptionfourniture'),
              }    
