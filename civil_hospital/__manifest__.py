# -*- coding: utf-8 -*-
{
    'name': "civil_hospital",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website','mail','base_automation'],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/groups.xml",

        "reports/report_hospital_appointment_templates.xml",
        "reports/report_hospital_appointment.xml",
        "reports/patient_template.xml",

        
        "data/server_action_data.xml",
        "data/scheduled_action_data.xml",
        "data/medicine_data.xml",
        "data/patient_data.xml",
        "data/template/mail_template.xml",
        "data/template/sms_template.xml",

        "views/appointment_form.xml",
        "views/patient_form.xml",
        "views/main_physician_views.xml",
        "views/external_api_integration_views.xml",
        "views/physician_speciality_views.xml",
        "views/hospital_physician_views.xml",
        "views/hospital_appointment_views.xml",
        "views/hospital_patient_views.xml",
        "views/civil_hospital_views.xml",
        "views/hospital_medicine_views.xml",
        "views/hospital_treatment_views.xml",
        "views/hospital_medication_views.xml",

        "wizard/appointment_wizard_views.xml",
        
    ],
    'license': 'LGPL-3',

    'demo': [
        'demo/demo.xml',


        
    ],
   

}

