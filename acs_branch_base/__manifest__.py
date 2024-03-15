# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════════╗
#║                                                                      ║
#║                  ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                   ║
#║                  ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                   ║
#║                  ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                   ║
#║                  ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                   ║
#║                  ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                   ║
#║                  ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                   ║
#║                            ╔═╝║     ╔═╝║                             ║
#║                            ╚══╝     ╚══╝                             ║
#║                  SOFTWARE DEVELOPED AND SUPPORTED BY                 ║
#║                ALMIGHTY CONSULTING SOLUTIONS PVT. LTD.               ║
#║                      COPYRIGHT (C) 2016 - TODAY                      ║
#║                      https://www.almightycs.com                      ║
#║                                                                      ║
#╚══════════════════════════════════════════════════════════════════════╝
{
    'name': 'Multiple Branch / Unit Operation Base for Odoo Applications',
    'version': '1.0.1',
    'category': 'sale',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': 'info@almightycs.com',
    'summary': """Multiple Branch / Unit Operation Base for Odoo Applications""",
    'description': """Multiple Branch / Unit Operation Base for Odoo Applications""",
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1', 
    "depends": ['base','web'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/branch_view.xml',
        'views/res_user_view.xml',
        'views/partner_view.xml',
        'views/menu_item.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'acs_branch_base/static/src/js/acs_branch_service.js',
            'acs_branch_base/static/src/js/acs_switch_branch.js',
            'acs_branch_base/static/src/xml/acs_switch_branch.xml',
        ],
    },
    'images': [
        'static/description/almightycs_odoo_multi_branch.png',
    ],
    'installable': True,
    'application': False,
    'sequence': 2,
    'price': 36,
    'currency': 'USD',
    'post_init_hook': '_set_branch',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: