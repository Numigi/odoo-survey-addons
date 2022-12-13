# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestSurveyLabelConstraint(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Make the option #1 of question #1 point to the page #2
        cls.env.ref('survey_condition.choice_1_1_1').sudo().write({
            'skip_option': 'specific_page',
            'skip_option_page_id': cls.env.ref('survey.survey_feedback_p1').id,
        })

    def test_ifPageIsBoundToSkipOption_thenCannotMoveThePageToOtherSurvey(self):
        new_survey = self.env['survey.survey'].sudo().create({'title': 'New Survey'})

        page_2 = self.env.ref('survey.survey_feedback_p1_q1')

        with self.assertRaises(ValidationError):
            page_2.survey_id = new_survey

    def test_ifPageIsBoundToSkipOption_thenCannotMoveTheQuestionToOtherSurvey(self):
        new_survey = self.env['survey.survey'].create({'title': 'New Survey'})

        # The page (#1) that contains the option that points to page #2
        page_1 = self.env.ref('survey.survey_feedback_p1_q1')
        print(page_1.survey_id.id,new_survey.id)
        with self.assertRaises(ValidationError):
            page_1.survey_id = new_survey
