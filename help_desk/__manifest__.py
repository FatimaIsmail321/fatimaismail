# -*- coding: utf-8 -*-
{
    'name': "Help Desk",
    'author': "Fatima Ismail",
    'website': "Help Desk",

    'category': 'HR',
    'version': '0.15',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

   
    'data': [
        'security/ir.model.access.csv',
        'security/group_helpdesk_security.xml',
        'data/data.xml',
       
        'views/help_desk.xml',
       
    ],
    'demo': [],
}
