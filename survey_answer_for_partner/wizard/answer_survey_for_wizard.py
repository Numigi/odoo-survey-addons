# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

import werkzeug
from odoo import fields, models

_logger = logging.getLogger(__name__)

"""
The type of survey input should be `manually` in this module's use case.

If the input is created, but the user quits before sending the answers,
it will be garbage collected by a cron automatically.
"""


class SurveyAnswerForPartnerWizard(models.TransientModel):
    _name = 'survey.answer.for.partner.wizard'
    _description = 'Survey Answer For Partner Wizard'

    survey_id = fields.Many2one('survey.survey', 'Survey')
    partner_id = fields.Many2one('res.partner', 'Partner')

    def action_validate(self):
        user = self.env.user
        public_groups = self.env.ref("base.group_public", raise_if_not_found=False)
        if public_groups:
            public_users = public_groups.sudo().with_context(active_test=False).mapped("users")
            user = public_users[0]
        user_input_id = self.survey_id.sudo()._create_answer(user=user, partner=self.partner_id)
        url1 = '/survey/partner/%s' % self.survey_id.access_token
        url = '%s?%s' % (
            url1, werkzeug.urls.url_encode({'answer_token': user_input_id and user_input_id.access_token or None}))
        return {
            'type': 'ir.actions.act_url',
            'name': "Start Survey",
            'target': 'self',
            'url': url,
        }
