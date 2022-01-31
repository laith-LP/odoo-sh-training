# -*- coding: utf-8 -*-
{
    'name': "My Library",  # Module title
    'summary': "Manage books easily",  # Module subtitle phrase
    'description': """
Manage Library
==============
Description related to library.
    """,  # Supports reStructuredText(RST) format
    'author': "Laith Al-Zoubi",
    'category': 'Demo',
    'version': '14.0.1',

    # Odoo modules which must be loaded before this one
    'depends': [
        'base',
        'web',
        'web_tour',
        'board',
    ],

    # List of data files which must always be installed or updated with the module
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'data/books_scheduled_actions.xml',
        'report/books_report.xml',
    ],
    # 'demo': [
    #     'demo/demo.xml'
    # ],
}