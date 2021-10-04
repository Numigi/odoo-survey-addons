# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestSurveyLabelConstraint(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Make the option #1 of question #1 point to the page #2
        cls.env.ref('survey.choice_1_1_1').write({
            'skip_option': 'specific_page',
            'skip_option_page_id': cls.env.ref('survey.feedback_2').id,
        })

    def test_ifPageIsBoundToSkipOption_thenCannotMoveThePageToOtherSurvey(self):
        new_survey = self.env['survey.survey'].create({'title': 'New Survey'})

        page_2 = self.env.ref('survey.feedback_2')

        with self.assertRaises(ValidationError):
            page_2.survey_id = new_survey

    def test_ifPageIsBoundToSkipOption_thenCannotMoveTheQuestionToOtherSurvey(self):
        new_survey = self.env['survey.survey'].create({'title': 'New Survey'})

        # The page (#1) that contains the option that points to page #2
        page_1 = self.env.ref('survey.feedback_1')

        with self.assertRaises(ValidationError):
            page_1.survey_id = new_survey
