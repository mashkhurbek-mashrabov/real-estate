{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Sales/CRM',
    'sequence': 1,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'license': "LGPL-3",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/res_user_views.xml',
        'views/estate_property_menu.xml'
    ],
    'installable': True,
    'application': True,
}
