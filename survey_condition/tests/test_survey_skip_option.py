# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestSurveySkipOption(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env.ref('survey.feedback_form')
        cls.user = cls.env.ref('base.demo_user0')
        cls.user_input = cls.env['survey.user_input'].create({
            'survey_id': cls.survey.id,
        })

        cls.page_1 = cls.env.ref('survey.feedback_1')
        cls.page_2 = cls.env.ref('survey.feedback_2')
        cls.page_3 = cls.env.ref('survey.feedback_3')
        cls.page_4 = cls.env.ref('survey.feedback_4')

        # Make questions 1.2, 3.1 and 4.1 simple_choice instead of multiple_choice
        questions = (
            cls.env.ref('survey.feedback_1_2') | cls.env.ref('survey.feedback_3_1') |
            cls.env.ref('survey.feedback_4_1')
        )
        questions.write({'type': 'simple_choice'})

        # Page 1
        cls.input_line_1_1 = cls.env['survey.user_input_line'].create({
            'user_input_id': cls.user_input.id,
            'question_id': cls.env.ref('survey.feedback_1_1').id,
            'value_suggested': cls.env.ref('survey.choice_1_1_1').id,
            'answer_type': 'suggestion',
        })
        cls.input_line_1_2 = cls.env['survey.user_input_line'].create({
            'user_input_id': cls.user_input.id,
            'question_id': cls.env.ref('survey.feedback_1_2').id,
            'value_suggested': cls.env.ref('survey.choice_1_2_1').id,
            'answer_type': 'suggestion',
        })

        # Page 2
        cls.input_line_2_6 = cls.env['survey.user_input_line'].create({
            'user_input_id': cls.user_input.id,
            'question_id': cls.env.ref('survey.feedback_2_6').id,
            'value_suggested': cls.env.ref('survey.choice_2_6_1').id,
            'answer_type': 'suggestion',
        })

        # Page 3
        cls.input_line_3_1 = cls.env['survey.user_input_line'].create({
            'user_input_id': cls.user_input.id,
            'question_id': cls.env.ref('survey.feedback_3_1').id,
            'value_suggested': cls.env.ref('survey.choice_3_1_1').id,
            'answer_type': 'suggestion',
        })

        cls.input_line_3_2 = cls.env['survey.user_input_line'].create({
            'user_input_id': cls.user_input.id,
            'question_id': cls.env.ref('survey.feedback_3_1').id,
            'value_free_text': 'Text value for page 3, question 2',
            'answer_type': 'free_text',
        })

        cls.input_line_3_3 = cls.env['survey.user_input_line'].create({
            'user_input_id': cls.user_input.id,
            'question_id': cls.env.ref('survey.feedback_3_1').id,
            'value_free_text': 'Text value for page 3, question 3',
            'answer_type': 'free_text',
        })

    def _get_next_page(self, current_page, go_back=False):
        return self.env['survey.survey'].next_page(
            self.user_input, current_page.id, go_back=go_back)

    def test_ifNoSkipOption_thenNextPageSelected(self):
        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (self.page_2, 1, False))

        values = self._get_next_page(self.page_2)
        self.assertEqual(values, (self.page_3, 2, False))

        values = self._get_next_page(self.page_3)
        self.assertEqual(values, (self.page_4, 3, True))

        values = self._get_next_page(self.page_4)
        self.assertEqual(values, (None, -1, False))

    def test_ifSkipNextFromPage1_thenNextPageIsPage3(self):
        choice = self.env.ref('survey.choice_1_1_1')
        choice.skip_option = 'skip_page'

        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (self.page_3, 2, False))

    def test_ifSkipNextFromPage2_thenNextPageIsPage4(self):
        choice = self.env.ref('survey.choice_2_6_1')
        choice.skip_option = 'skip_page'

        values = self._get_next_page(self.page_2)
        self.assertEqual(values, (self.page_4, 3, True))

    def test_ifSkipNextFromPage3_thenNextPageIsNone(self):
        choice = self.env.ref('survey.choice_3_1_1')
        choice.skip_option = 'skip_page'

        values = self._get_next_page(self.page_3)
        self.assertEqual(values, (None, -1, False))

    def test_ifSkipNextFromPage4_thenNextPageIsNone(self):
        choice = self.env.ref('survey.choice_4_1_1')
        choice.skip_option = 'skip_page'

        values = self._get_next_page(self.page_4)
        self.assertEqual(values, (None, -1, False))

    def test_ifSkipFromPage1To3_thenLastPageIsFalse(self):
        choice = self.env.ref('survey.choice_1_1_1')
        choice.write({
            'skip_option': 'specific_page',
            'skip_option_page_id': self.page_3.id,
        })

        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (self.page_3, 2, False))

    def test_ifSkipFromPage1To4_thenLastPageIsTrue(self):
        choice = self.env.ref('survey.choice_1_1_1')
        choice.write({
            'skip_option': 'specific_page',
            'skip_option_page_id': self.page_4.id,
        })

        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (self.page_4, 3, True))

    def test_ifSendFormFromPage1_thenNextPageisNone(self):
        choice = self.env.ref('survey.choice_1_1_1')
        choice.skip_option = 'send_form'

        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (None, -1, False))

    def test_ifMultipleSkipOptions_thenLastOptionIsSelected(self):
        choice = self.env.ref('survey.choice_1_1_1')
        choice.skip_option = 'send_form'

        choice = self.env.ref('survey.choice_1_2_1')
        choice.skip_option = 'skip_page'

        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (self.page_3, 2, False))

    def test_skipOptionsOnPage2_hasNoImpactOnPage1(self):
        choice = self.env.ref('survey.choice_1_1_1')
        choice.skip_option = 'send_form'

        choice = self.env.ref('survey.choice_2_6_1')
        choice.skip_option = 'skip_page'

        values = self._get_next_page(self.page_1)
        self.assertEqual(values, (None, -1, False))

    def test_go_back_after_page_skip(self):
        self.user_input.add_page_to_history(self.page_1)
        values = self._get_next_page(self.page_3, go_back=True)
        self.assertEqual(values, (self.page_1, 0, False))

    def test_go_back_twice_after_page_skip(self):
        self.user_input.add_page_to_history(self.page_1)
        self.user_input.add_page_to_history(self.page_3)

        values = self._get_next_page(self.page_4, go_back=True)
        self.assertEqual(values, (self.page_3, 2, False))

        self.user_input.pop_previous_page()

        values = self._get_next_page(self.page_3, go_back=True)
        self.assertEqual(values, (self.page_1, 0, False))
