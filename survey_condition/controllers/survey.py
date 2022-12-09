# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import logging

from odoo import http, SUPERUSER_ID
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request

_logger = logging.getLogger(__name__)


fill_survey_decorator = http.route(
    ['/survey/fill/<model("survey.survey"):survey>/<string:token>',
     '/survey/fill/<model("survey.survey"):survey>/<string:token>/<string:prev>'],
    type='http', auth='public', website=True)


class SurveyWithSkipConditions(Survey):

    @http.route(['/survey/submit/<model("survey.survey"):survey>'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit(self, survey, **post):
        """Set the state of the survey to completed_but_not_sent if required.

        When the survey is completed but the last page seen is not the last page
        of the survey, the state is set to completed_but_not_sent.

        The method was completely overiddre because it could not be properly inherited.

        The original method can be found at
        https://github.com/odoo/odoo/blob/11.0/addons/survey/controllers/main.py#L207
        """
        env = request.env

        _logger.debug('Incoming data: %s', post)
        page_id = int(post['page_id'])
        questions = env['survey.question'].search([('page_id', '=', page_id)])

        errors = {}
        for question in questions:
            answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
            errors.update(question.validate_question(post, answer_tag))

        ret = {}
        if len(errors):
            ret['errors'] = errors
        else:
            try:
                user_input = env['survey.user_input'].sudo().search(
                    [('token', '=', post['token'])], limit=1)
            except KeyError:
                return request.render("website.403")

            user_id = env.user.id if user_input.type != 'link' else SUPERUSER_ID

            for question in questions:
                answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
                env['survey.user_input_line'].with_user(user=user_id).save_lines(
                    user_input.id, question, post, answer_tag)

            go_back = post['button_submit'] == 'previous'

            next_page, _, last = env['survey.survey'].next_page(
                user_input, page_id, go_back=go_back)

            vals = {'last_displayed_page_id': page_id}

            ##############################################
            # Only the following block was modified
            ##############################################
            last_displayed_page = env['survey.page'].browse(page_id)

            if not go_back:
                user_input.add_page_to_history(last_displayed_page)

            last_displayed_is_last_page = (
                last_displayed_page == last_displayed_page.survey_id.page_ids[-1]
            )
            survey_is_completed = next_page is None and not go_back

            if last_displayed_is_last_page and survey_is_completed:
                vals.update({'state': 'done'})
            elif not last_displayed_is_last_page and survey_is_completed:
                vals.update({'state': 'completed_but_not_sent'})
            else:
                vals.update({'state': 'skip'})

            ##############################################
            # Modified block ends here
            ##############################################

            user_input.with_user(user=user_id).write(vals)
            ret['redirect'] = '/survey/fill/%s/%s' % (survey.id, post['token'])

            if go_back:
                ret['redirect'] += '/prev'

        return json.dumps(ret)

    @fill_survey_decorator
    def fill_survey(self, survey, token, prev=None, **post):
        """If the survey is completed but not done, render the confirmation page."""
        user_input = self._get_user_input_from_token(token)
        if not user_input:
            return request.render("website.403")

        if user_input.state == 'completed_but_not_sent':
            return request.render(
                'survey_condition.send_confirmation_page',
                {'survey': survey, 'token': token, 'user_input': user_input})

        return super().fill_survey(survey=survey, token=token, prev=prev, **post)

    @http.route(['/survey/completed/<string:token>'],
                type='http', methods=['POST'], auth='public', website=True)
    def submit_from_completed_page(self, token, **post):
        user_input = self._get_user_input_from_token(token)
        if not user_input:
            return request.render("website.403")

        go_back = post['button_submit'] == 'previous'

        if go_back:
            return json.dumps({
                'redirect': '/survey/go_back_from_completed_page/{token}'.format(
                    token=user_input.token)
            })
        else:
            user_input.state = 'done'
            return json.dumps({
                'redirect': '/survey/fill/{survey_id}/{token}'.format(
                    survey_id=user_input.survey_id.id, token=user_input.token)
            })

    @http.route(['/survey/go_back_from_completed_page/<string:token>'],
                type='http', auth='public', website=True)
    def go_back_from_completed_page(self, token, **post):
        user_input = self._get_user_input_from_token(token)
        if not user_input:
            return request.render("website.403")

        user_input.state = 'skip'

        page = user_input.last_displayed_page_id
        page_number = list(page.survey_id.page_ids).index(page)

        data = {
            'survey': page.survey_id,
            'page': page,
            'page_nr': page_number,
            'token': user_input.token,
        }

        is_last_page = page == page.survey_id.page_ids[-1]
        if is_last_page:
            data.update({'last': True})

        return request.render('survey.survey', data)

    @staticmethod
    def _get_user_input_from_token(token):
        return request.env['survey.user_input'].sudo().search([('token', '=', token)], limit=1)


class SurveyWithPopPageHistoryLine(Survey):
    """When the user clicks on the previous button, remove one entry from the history.

    Each time the user clicks on previous, he is forwarded one step back recursively.
    """

    @fill_survey_decorator
    def fill_survey(self, survey, token, prev=None, **post):
        result = super().fill_survey(survey=survey, token=token, prev=prev, **post)

        if prev:
            user_input = self._get_user_input_from_token(token)
            if user_input:
                user_input.pop_previous_page()

        return result
