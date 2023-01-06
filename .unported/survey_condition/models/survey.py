# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class SurveyWithSkipConditions(models.Model):

    _inherit = 'survey.survey'

    @api.model
    def next_page(self, user_input, page_id, go_back=False):
        """Check for any anwser with a skip option when searching for the next page.

        The question inputs are checked in the reversed order so that the last
        questions are prioritized.

        If any input with a skip option is found, the rule for that option is applied
        instead of the standard algorithm.
        """
        current_page = self.env['survey.page'].browse(page_id)

        reversed_page_input_lines = (
            user_input.user_input_line_ids
            .filtered(lambda l: l.page_id == current_page)
            .sorted(key=lambda l: -l.question_id.sequence)
        )

        value_with_skip_option = next((
            l.value_suggested for l in reversed_page_input_lines
            if l.question_id.type == 'simple_choice' and l.value_suggested.skip_option
        ), None)

        if value_with_skip_option is not None:
            return self._get_next_page_from_skip_option(
                current_page,
                option=value_with_skip_option.skip_option,
                specific_page=value_with_skip_option.skip_option_page_id)

        else:
            return super().next_page(user_input=user_input, page_id=page_id, go_back=go_back)

    def _get_next_page_from_skip_option(self, current_page, option, specific_page):
        if option == 'send_form':
            # Send the form
            return (None, -1, False)

        elif option == 'skip_page':
            return self._get_next_page_from_skip_option_skip_page(current_page)

        elif option == 'specific_page':
            return self._get_next_page_from_skip_option_specific_page(current_page, specific_page)

        else:
            raise ValidationError(_(
                'Could not evaluate the next page for the survey {survey}. '
                'Invalid skip option {option}.'
            ).format(survey=current_page.survey_id.display_name, option=option))

    @staticmethod
    def _get_next_page_from_skip_option_skip_page(current_page):
        pages = list(current_page.survey_id.page_ids)

        # If the current page is last or the next page is last, then send the form
        if current_page in pages[-2:]:
            return (None, -1, False)

        else:
            current_page_index = pages.index(current_page)
            next_page_index = current_page_index + 2
            is_last_page = next_page_index == len(pages) - 1
            return (pages[next_page_index], next_page_index, is_last_page)

    @staticmethod
    def _get_next_page_from_skip_option_specific_page(current_page, specific_page):
        pages = list(current_page.survey_id.page_ids)
        specific_page_index = pages.index(specific_page)
        specific_page_is_last = specific_page_index == len(pages) - 1
        return (specific_page, specific_page_index, specific_page_is_last)


class SurveyWithGoBackAfterSkipingPage(models.Model):

    _inherit = 'survey.survey'

    @api.model
    def next_page(self, user_input, page_id, go_back=False):
        """When the user clicked on `Go Back`, the last page from the history is returned."""
        if go_back:
            return self._get_previous_page(user_input)
        else:
            return super().next_page(user_input=user_input, page_id=page_id, go_back=False)

    @staticmethod
    def _get_previous_page(user_input):
        """Get a tuple reprensenting the last page seen by the user."""
        previous_page = user_input.get_previous_page()

        if not previous_page:
            previous_page = user_input.survey_id.page_ids[0]

        pages = list(user_input.survey_id.page_ids)
        page_index = pages.index(previous_page)
        return (previous_page, page_index, False)
