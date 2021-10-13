# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SurveyUserInputWithStateCompletedNotSent(models.Model):

    _inherit = 'survey.user_input'

    state = fields.Selection(selection_add=[('completed_but_not_sent', 'Completed But Not Sent')])


class SurveyInputWithPreviousPage(models.Model):

    _inherit = 'survey.user_input'

    def pop_previous_page(self):
        """Pop the last page seen from the page history of the user input.

        :return: the last seen page (survey.page)
        """
        history_line = self._get_previous_history_line()
        page = history_line.mapped('page_id')
        history_line.unlink()
        return page

    def get_previous_page(self):
        """Get the last page seen from the page history of the user input.

        :return: the last seen page (survey.page)
        """
        history_line = self._get_previous_history_line()
        return history_line.mapped('page_id')

    def _get_previous_history_line(self):
        return self.env['survey.user_input.page.history'].search(
            [('input_id', '=', self.id)], order='id desc', limit=1)

    def add_page_to_history(self, page):
        """Add a page to the user input's history.

        :param page: the survey page to add (survey.page)
        """
        self.env['survey.user_input.page.history'].create({
            'input_id': self.id,
            'page_id': page.id,
        })


class SurveyUserInputPageHistory(models.Model):

    _name = 'survey.user_input.page.history'

    input_id = fields.Many2one(
        'survey.user_input', 'Input', required=True, index=True, ondelete='cascade')
    page_id = fields.Many2one('survey.page', 'Page')
