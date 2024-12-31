{
    "name": "First_app",
    'author': 'Dharmik',
    'license': 'LGPL-3',
    'depends': [
        'mail',
        'product',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/face_detaction_wizard_view.xml',
        'wizard/img_wizard_view.xml',
        'views/inher_view.xml',
        'views/img.xml',
        'views/attendance_views.xml',
        'views/appointment_line.xml',
        'views/sec_view.xml',
        'views/record_user.xml',
        'views/user.xml',
        'views/menu.xml',
        'views/user_tag_views.xml',
        'views/res_config_settings_view.xml',
        'report/test_demo.xml',
        'report/employee_report.xml',
        'report/report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'static/src/js/your_module.js',
        ],
    },
    'installable': True,
}
