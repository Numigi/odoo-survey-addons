# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import uuid
from odoo import api, fields, models
from odoo.addons.base.models.res_partner import Partner
from odoo.addons.survey.models.survey import Survey, SurveyUserInput
from odoo.tools import pycompat


"""
The type of survey input should be `manually` in this module's use case.

If the input is created, but the user quits before sending the answers,
it will be garbage collected by a cron automatically.
"""
SURVEY_INPUT_TYPE = 'manually'


def _generate_survey_input_token() -> str:
    """Generate a token for a survey input.

    This function reproduces the behavior found in Odoo for survey invitations
    sent by email.

    See function create_token of odoo/addons/survey/wizard/survey_email_compose_message.py.
    """
    return pycompat.text_type(uuid.uuid4())


def create_survey_input_for_partner(survey: Survey, partner: Partner) -> SurveyUserInput:
    """Create a user input for the given survey and partner.

    :param survey: the survey to answer.
    :param partner: the partner for whom to answer for.
    :return: the user input
    """
    return survey.env['survey.user_input'].create({
        'survey_id': survey.id,
        'date_create': fields.Datetime.now(),
        'type': SURVEY_INPUT_TYPE,
        'state': 'new',
        'token': _generate_survey_input_token(),
        'partner_id': partner.id,
    })


class SurveyAnswerForPartnerWizard(models.TransientModel):

    _name = 'survey.answer.for.partner.wizard'
    _description = 'Survey Answer For Partner Wizard'

    survey_id = fields.Many2one('survey.survey', 'Survey')
    partner_id = fields.Many2one('res.partner', 'Partner')

    def action_validate(self):
        """Open the website page with the survey answered for the partner.

        This method was inpired and adapted from the method action_test_survey
        of survey.survey defined in odoo/addons/survey/models/survey.py.
        """
        url = self.survey_id.with_context(relative_url=True).public_url
        user_input = create_survey_input_for_partner(self.survey_id, self.partner_id)
        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": "{}/{}".format(url, user_input.token)
        }
