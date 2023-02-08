# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestPartnerSmartButton(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env.ref('survey.survey_feedback')
        cls.partner_1 = cls.env['res.partner'].create({'name': 'Partner'})
        cls.partner_2 = cls.env['res.partner'].create({'name': 'Partner 2'})

    @classmethod
    def _generate_answer(cls, partner):
        wizard = cls.env['survey.answer.for.partner.wizard'].create({
            'survey_id': cls.survey.id,
            'partner_id': partner.id,
        })
        wizard.action_validate()

    def test_survey_answers_count(self):
        self._generate_answer(self.partner_1)
        assert self.partner_1.survey_answers_count == 1
        assert self.partner_2.survey_answers_count == 0

    def test_if_parent_partner__child_partner_surveys_included(self):
        self.partner_1.parent_id = self.partner_2
        self._generate_answer(self.partner_1)
        assert self.partner_1.survey_answers_count == 1
        assert self.partner_2.survey_answers_count == 1
