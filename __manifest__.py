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
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_stage_view.xml',
        'views/vm_student_views.xml',
    ],
    'images': [
        'static/description/logo_1.jpg',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}