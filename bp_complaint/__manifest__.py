{
    'name': 'BP Complaint',
    'summary': 'Complaint website feature',
    'description': "",
    'version': '16.0.1.0.0',
    'license': 'Other proprietary',
    'category': 'Website',
    "author": "Ilyas",
    'depends': ['website', 'l10n_din5008'],
    'data': [
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'views/bp_complaint.xml',
        'data/complaint_types.xml',
        'data/sequence.xml',
        'data/mail_template.xml',
        'views/res_config_settings_views.xml',
        'report/workorder_report.xml',
    ],
    'assets': {
        'web.assets_tests': [
            'bp_complaint/static/tests/tours/complaint.js',
        ],
    },
    'installable': True,
    'application': True,
}
