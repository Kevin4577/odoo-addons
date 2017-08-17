# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Invoice Customer Reference',
    'version': '10.0.1.0.0',
    'category': 'Account',
    'summary': """This module specifies invoice reference for customer when
    state of invoice was draft, and allow customer maintain manually.""",
    'author': "Elico Corp",
    'website': 'www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_invoice.xml',
    ],
    'installable': True,
    'auto_install': False,
}
