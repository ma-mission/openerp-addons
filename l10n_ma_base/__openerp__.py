# -*- encoding: utf-8 -*-

{
    'name' : 'Maroc',
    'version' : '1.0',
    'author' : 'UH1',
    'category' : 'Localization',
    'description': """
Localization Module - Maroc
===========================
""",
    'website': 'http://www.uh1.ac.ma',
    'depends' : ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'data/res.country.state.csv',  # http://www.statoids.com/uma.html
        'data/res.city.csv',  # http://www.statoids.com/yma.html
    ],
    'demo' : [],
    'auto_install': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

