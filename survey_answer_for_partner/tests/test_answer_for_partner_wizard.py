# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestAnswerForPartnerWizard(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env.ref('survey.survey_feedback')
        cls.partner = cls.env['res.partner'].create({'name': 'Partner'})
        cls.user = cls.env['res.users'].create({
            'name': 'Test Surveys',
            'login': 'test_survey',
            'email': 'test_survey@test.com',
            'groups_id': [(4, cls.env.ref('survey.group_survey_user').id)],
        })

    def test_survey_input_has_the_selected_partner(self):
        wizard = self.env['survey.answer.for.partner.wizard'].with_user(self.user).create({
            'survey_id': self.survey.id,
            'partner_id': self.partner.id,
        })
        wizard.sudo().action_validate()
        last_answer = self.env['survey.user_input'].search([], order='create_date desc', limit=1)
        assert last_answer.partner_id == self.partner
