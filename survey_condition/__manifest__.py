# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Survey Skip Condition',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Survey',
    'summary': 'Add skip conditions to surveys.',
    'depends': ['survey'],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_question.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
