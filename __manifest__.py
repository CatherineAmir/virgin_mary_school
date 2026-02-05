# -*- coding: utf-8 -*-
{
    'name': 'Virgin Mary School',
    'version': '1.0',
    'summary': 'School Management System',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'Education',
    'author': 'SITA-EGYPT',
    'company': 'SITA-EGYPT',
    'maintainer': 'SITA-EGYPT',
    'website': 'https://sita-eg.com',
    'depends': ['base', 'mail', 'website', 'survey', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_stage_view.xml',
        'views/vm_student_views.xml',
        'views/student_grade_view.xml',
        'views/academic_year.xml',
        "views/parent_relationship_view.xml",
        'views/res_partner.xml',
        'views/parent_view.xml',
        'views/res_company.xml',
        "templates/student_application_template.xml",
        "views/menus.xml",

    ],
    'images': [
        "static/description/logo_1.png"
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
