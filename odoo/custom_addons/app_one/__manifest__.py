{
    'name': 'App One',
    'author': 'LAKHSAM Ahmed',
    'category': 'Custom',
    'version': '1.0',
    'depends': ['base', 'sale_management', 'account', 'mail'],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
             'data/sequences.xml',
             'views/main_menu.xml',
             'views/property_view.xml',
             'views/property_history_view.xml',
             'views/owner_view.xml',
             'views/tag_view.xml',
             'views/sale_order_view.xml',
             'views/account_move_view.xml',
             'views/building_view.xml',
             'wizard/change_property_state_wizard_view.xml',
             'reports/property_report.xml'],
    'assets': {
        'web.assets_backend': ['app_one/static/src/css/property.css']
    },
    'application': True,
}