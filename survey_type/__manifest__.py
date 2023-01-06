# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Survey Type',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Survey',
    'summary': 'Enable typing a survey.',
    'depends': ['survey'],
    'data': [
        'views/survey.xml',
        'views/survey_type.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
