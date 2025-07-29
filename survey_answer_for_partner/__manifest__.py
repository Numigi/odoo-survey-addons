# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Survey Answer For Partner',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Survey',
    'summary': 'Allow answering a survey for someone else.',
    'depends': ['survey'],
    'data': [
        'answer_create_user.xml',
        'answer_survey_for_wizard.xml',
        'answer_survey_for_button.xml',
        'fix_back_to_survey.xml',
        'partner_smart_button.xml',
    ],
    'installable': True,
}
