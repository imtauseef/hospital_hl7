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
    'name': 'Multiple Branch/Unit Operation for Inventory',
    'version': '1.0.1',
    'category': 'stock',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': 'info@almightycs.com',
    'summary': """Multiple Branch/Unit Operation for Inventory""",
    'description': """Multiple Branch/Unit Operation for Inventory""",
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1', 
    "depends": ['stock','acs_branch_base','web','base'],
    "data": [
        'security/security.xml',
        'views/stock_location_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_warehouse_view.xml',
    ],
    'images': [
        'static/description/almightycs_odoo_multi_branch.png',
    ],
    'installable': True,
    'application': False,
    'sequence': 2,
    'price': 12,
    'currency': 'USD',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: