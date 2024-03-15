# -*- coding: utf-8 -*-
{
    'name': "HL7 Patient Registration",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nasrullah",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'acs_hms_base','acs_hms'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/nextkin_relation_data.xml',
        'data/res_partner_title_default_data.xml',
        'data/hospital_service_data.xml',
        'data/family_history_data.xml',
        'views/nextkin_relation.xml',
        'views/hl7_patient_registration.xml',
        'views/menu_item.xml'



    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
