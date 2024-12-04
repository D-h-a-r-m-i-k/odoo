{
    "name": "First_app",
    'author': 'Dharmik',
    'license': 'LGPL-3',
    'depends': [
        'mail',
        'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/img.xml',
        'views/attendance_views.xml',
        'views/appointment_line.xml',
        'views/sec_view.xml',
        'views/record_user.xml',
        'views/user.xml',
        'views/menu.xml',
        'views/user_tag_views.xml',
        'report/employee_report.xml',
        'report/report.xml',
    ],
    'installable': True,
}
