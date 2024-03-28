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
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_view.xml',
        'views/estate_inherited_user_view.xml',
        'views/estate_property_menu.xml'
    ],
    'installable': True,
    'application': True,
}
