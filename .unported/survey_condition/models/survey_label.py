# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SurveyLabelWithConstraintOnSkipOptionPage(models.Model):
    """Prevent a survey option from skiping to a page that belongs to a different suvrvey."""

    _name = 'survey.label'
    _rec_name = 'value'
    _order = 'sequence,id'
    _description = 'Survey Label'

    question_id = fields.Many2one('survey.question', string='Question', ondelete='cascade')
    question_id_2 = fields.Many2one('survey.question', string='Question 2', ondelete='cascade')
    sequence = fields.Integer('Label Sequence order', default=10)
    value = fields.Char('Suggested value', translate=True, required=True)
    quizz_mark = fields.Float('Score for this choice',
                              help="A positive score indicates a correct choice; a negative or null score indicates a wrong answer")


    skip_option = fields.Selection([
        ('skip_page', 'Skip Next Page'),
        ('specific_page', 'Go To Specific Page'),
        ('send_form', 'Send Form'),
    ], 'Skip Option')

    skip_option_page_id = fields.Many2one('survey.question', 'Page', domain=[('is_page', '=', True)],
                                          ondelete='restrict')

    @api.constrains('question_id', 'question_id_2')
    def _check_question_not_empty(self):
        """Ensure that field question_id XOR field question_id_2 is not null"""
        if not bool(self.question_id) != bool(self.question_id_2):
            raise ValidationError(_("A label must be attached to only one question."))

    skip_option_survey_id = fields.Many2one(
        'survey.survey', 'Skip Option Survey',
        related='skip_option_page_id.survey_id', store=True, readonly=True)

    question_survey_id = fields.Many2one(
        'survey.survey', 'Question Survey',
        related='question_id.page_id.survey_id', store=True, readonly=True)

    @api.constrains('skip_option_survey_id', 'question_survey_id', 'skip_option')
    def _check_specific_option_belons_to_same_survey(self):
        labels_with_skip_to_specific_page = self.filtered(
            lambda l: l.skip_option == 'specific_page')

        for label in labels_with_skip_to_specific_page:
            if label.skip_option_survey_id != label.question_survey_id:
                raise ValidationError(_(
                    'The question choice {choice} has a skip option '
                    'of the survey {skip_option_survey}. '
                    'This survey is different from the survey of '
                    'the question {question} ({question_survey}).'
                ).format(
                    choice=label.display_name,
                    question=label.question_id.display_name,
                    skip_option_survey=label.skip_option_survey_id.display_name,
                    question_survey=label.question_survey_id.display_name,
                ))

    @api.onchange('skip_option')
    def _onchange_skip_option_if_not_specific_page_empty_skip_option_page_id(self):
        if self.skip_option != 'specific_page':
            self.skip_option_page_id = None


class SurveyQuestion(models.Model):

        _inherit = 'survey.question'

        labels_ids = fields.One2many('survey.label', 'question_id', string='Types of answers', copy=True)
