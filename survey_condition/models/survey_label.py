# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SurveyLabelWithCondition(models.Model):

    _inherit = 'survey.label'

    skip_option = fields.Selection([
        ('skip_page', 'Skip Next Page'),
        ('specific_page', 'Go To Specific Page'),
        ('send_form', 'Send Form'),
    ], 'Skip Option')

    skip_option_page_id = fields.Many2one('survey.page', 'Page', ondelete='restrict')

    @api.onchange('skip_option')
    def _onchange_skip_option_if_not_specific_page_empty_skip_option_page_id(self):
        if self.skip_option != 'specific_page':
            self.skip_option_page_id = None


class SurveyLabelWithConstraintOnSkipOptionPage(models.Model):
    """Prevent a survey option from skiping to a page that belongs to a different suvrvey."""

    _inherit = 'survey.label'

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
                    'The question choice {choice} has a skip option to the {page} '
                    'of the survey {skip_option_survey}. '
                    'This survey is different from the survey of '
                    'the question {question} ({question_survey}).'
                ).format(
                    choice=label.display_name,
                    question=label.question_id.display_name,
                    skip_option_survey=label.skip_option_survey_id.display_name,
                    question_survey=label.question_survey_id.display_name,
                ))
