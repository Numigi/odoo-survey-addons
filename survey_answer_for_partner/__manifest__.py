# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Survey Answer For Partner',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Survey',
    'summary': 'Allow answering a survey for someone else.',
    'depends': ['survey'],
    'data': [
        'views/answer_create_user.xml',
        'wizard/answer_survey_for_wizard.xml',
        'views/answer_survey_for_button.xml',
        'views/fix_back_to_survey.xml',
        'views/partner_smart_button.xml',
        "security/ir.model.access.csv",
    ],
    'installable': True,
}
