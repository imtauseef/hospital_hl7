{
    'name': 'HL7 Patient Appointment',
    'version': '1.0',
    'summary': 'Brief summary of what the module does',
    'description': """
        Detailed description of the module's functionality.
        You can use multiple lines for the description.
    """,
    'category': 'Category/Industry',
    'author': 'Your Name',
    'website': 'Your Website URL',
    'depends': ['base', 'acs_hms', 'hl7_patient_appointment'],  # List of dependencies
    'data': [
        'views/hl7_patient_appointment.xml',
        # 'security/ir.model.access.csv', 
        # Add other data files here (e.g., data files, security rules)
    ],
    'demo': [
        'demo/demo_data.xml',  # Demo data for the module
    ],
    'installable': True,  # Whether the module can be installed or not
    'auto_install': False,  # Whether the module should be auto-installed
}
